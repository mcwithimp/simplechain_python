from typing import Iterable
from .blockchain import Block, pushBlock, getHead, getBlockchain, BlockHeader, getTimestamp, myKey
from .transaction import createCoinbaseTx, Transaction
from ..lib.crypto import generateHash
from .miner import mine, minerInterrupt


# 웹소켓용
import asyncio
import websockets
from .socket import bootstrap, handler, createMessage
import json
import os
import threading

PORT = os.environ.get('PORT', 9999)
BOOTSTRAP_PEER = os.environ.get('BOOTSTRAP_PEER', '')


async def node():
    # 채굴 쓰레드에서 채굴 완료 이벤트를 받을 이벤트 큐 생성
    q = asyncio.Queue()
    loop = asyncio.get_event_loop()

    # 채굴 쓰레드 생성
    threading.Thread(target=minerThread, daemon=True, args=(q,loop,)).start()

    await asyncio.gather(
        bootstrapTask(),
        networkTask(),
        pushBlockTask(q)
    )

def bootstrapTask():
    if any(BOOTSTRAP_PEER):
        split = BOOTSTRAP_PEER.split(':')
        return bootstrap(address=split[0], port=split[1])

    # never resolving 
    return asyncio.Future()


def networkTask():
    print(f"wss at {PORT}")
    return websockets.serve(handler, "0.0.0.0", PORT)

async def pushBlockTask(queue):
    while True:
        nextBlock = await queue.get()
        pushBlock(nextBlock)
        queue.task_done()


def minerThread(queue,loop):

    async def miner():
        while True:
            asyncio.run_coroutine_threadsafe(queue.join(), loop=loop).result()

            currentHead = getHead()
            currentLevel = currentHead["header"]["level"]
            coinbaseTx = createCoinbaseTx(
                pk=myKey["pk"],
                sk=myKey["sk"],
                level=currentLevel + 1)
            transactions = [coinbaseTx]

            # 이번에 생성하는 블록 헤더를 만든다
            header = BlockHeader(
                level=currentLevel + 1,
                previousHash=currentHead["hash"],
                timestamp=getTimestamp(),
                miner=myKey["pk"],
                merkleRoot=generateHash(transactions),
                nonce=0,
                difficulty=currentHead["header"]["difficulty"]
            )

            # 채굴 시작
            print("Mining", currentHead["header"]["level"])
            mineResult = mine(header, getBlockchain())

            # 다른 노드가 채굴을 먼저 완료헀을 때에는 mine() 함수가 None을 리턴함
            # 이럴 경우 pushBlock을 하지 않는다
            if mineResult is None:
                continue

            # 내가 찾은 블록일때만 pushBlock 실행
            block = Block(
                hash=mineResult["blockHash"],
                header=mineResult["header"],
                transactions=transactions
            )

            # 만든 블록을 큐에 삽입
            asyncio.run_coroutine_threadsafe(queue.put(block), loop=loop).result()

    asyncio.run(miner())


if __name__ == '__main__':
    asyncio.run(node())
