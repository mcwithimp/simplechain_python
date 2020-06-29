from typing import Iterable
from .blockchain import Block, pushBlock, getHead, getBlockchain, BlockHeader, getTimestamp, myKey
from .transaction import createCoinbaseTx, Transaction
from ..lib.crypto import generateHash
from .miner import mine, minerInterrupt
from .rpc import app


# 웹소켓용
import asyncio
import websockets
from .socket import bootstrap, handler, createMessage
import json
import os
import threading

PORT = os.environ.get('PORT', 9999)
BOOTSTRAP_PEER = os.environ.get('BOOTSTRAP_PEER', '')

mempool: Iterable[Transaction] = []


def node():
    eventloop = asyncio.get_event_loop()

    # 부트스트랩
    bootstrapThread()

    # 채굴 쓰레드 생성
    threading.Thread(target=minerThread, daemon=True).start()

    # 소켓 서버 쓰레드
    socketThread()

    # rpc
    app.run(host='0.0.0.0', port=1337)

    # eventloop.run_until_complete(boot)
    # eventloop.run_until_complete(sock)
    eventloop.run_forever()


def bootstrapThread():
    if any(BOOTSTRAP_PEER):
        split = BOOTSTRAP_PEER.split(':')
        bootstrap(address=split[0], port=split[1])


def socketThread():
    eventloop = asyncio.get_event_loop()
    eventloop.run_until_complete(websockets.serve(handler, "0.0.0.0", PORT))


def minerThread():
    while True:
        currentHead = getHead()
        currentLevel = currentHead["header"]["level"]
        coinbaseTx = createCoinbaseTx(
            pk=myKey["pk"],
            sk=myKey["sk"],
            level=currentLevel + 1)
        transactions = [coinbaseTx, *mempool]

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
            pass

        # 내가 찾은 블록일때만 pushBlock 실행
        block = Block(
            hash=mineResult["blockHash"],
            header=mineResult["header"],
            transactions=transactions
        )

        pushBlock(block)


if __name__ == '__main__':
    node()
