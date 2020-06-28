from typing import Iterable
from .blockchain import Block, pushBlock, getHead, getBlockchain, BlockHeader, getTimestamp, myKey
from .transaction import createCoinbaseTx, Transaction
from ..lib.crypto import generateHash
from .miner import mine
import threading

mempool: Iterable[Transaction] = []
# 마이닝 쓰레드 이벤트 핸들러
minerInterrupt = threading.Event()

# def connectBlock(block):
#     if (not doing_reorg and reorg_if_necessary()) or \
#             chain_idx == ACTIVE_CHAIN_IDX:
#         mine_interrupt.set()
#         logger.info(
#             f'block accepted '
#             f'height={len(active_chain) - 1} txns={len(block.txns)}')


def node():
    threading.Thread(target=minerThread).start()


def minerThread():
    while True:
        currentHead = getHead()
        currentLevel = currentHead["header"]["level"]
        print(currentHead)
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
