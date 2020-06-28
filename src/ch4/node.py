from typing import Iterable
from .blockchain import Block, pushBlock, getHead, getBlockchain, BlockHeader, getTimestamp, myKey
from .transaction import createCoinbaseTx, Transaction
from ..lib.crypto import generateHash
from .miner import mine
import threading

mempool: Iterable[Transaction] = []

# 마이닝 쓰레드 이벤트 핸들러
minerInterrupt = threading.Event()


def node():
    # 채굴 쓰레드 생성
    threading.Thread(target=minerThread).start()


def minerThread():
    while True:
        currentHead = getHead()
        currentLevel = currentHead["header"]["level"]
        # print(currentHead)
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
            txsHash=generateHash(transactions),
            nonce=0,
            difficulty=currentHead["header"]["difficulty"]
        )

        # 채굴 시작
        print("Mining", currentHead["header"]["level"])
        mineResult = mine(header, getBlockchain(), minerInterrupt)

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
