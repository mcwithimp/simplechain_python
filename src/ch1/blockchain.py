import json
import os
import sys
import time
from typing import Iterable, NamedTuple, TypedDict
from ..lib.crypto import getKeys, generateHash

Transaction = str


class BlockHeader(TypedDict):
    # 현재 블록의 레벨(=높이)
    level: int

    # 이전 블록의 해시
    previousHash: str

    # 현재 블록의 타임스탬프
    timestamp: int

    # 마이닝 정보
    # 1. 마이너: 비트코인에서는 코인베이스 트랜잭션으로 표기하고 별도의 miner 정보는 없음
    miner: str

    # 머클 트리의 해시 (txsHash)
    merkleRoot: str


class Block(TypedDict):
    # 블록 해시
    hash: str

    # 블록 헤더
    header: BlockHeader

    # 트랜잭션
    transactions: Iterable[Transaction]


Blockchain = Iterable[Block]


myKey = getKeys('mc')
"""
 "alias": "mc",
 "sk": "fc487a5adcb6fe82ac8de12f2c6cffa2b395bae0b694591c1a9ef973552e4030",
 "pk": "c621e37b2be6e83ce77b539a90f6fc99a218986499a5b7565283eb9ec369f5c08f527af268fa9a274613804f8773b042e1866a84c705ddc18bb6f05598d7456a",
 "pkh": "1G8RdTC6nSmuLVkBzkWEaWzqqsqM8f98cU"
"""


def getTimestamp() -> int:
    return int(time.time())


def createGenesisBlock() -> Block:
    transactions = ['Alice sends 10 btc to Bob']

    header = BlockHeader(
        level=0,
        previousHash='0' * 64,
        timestamp=getTimestamp(),
        miner='1G8RdTC6nSmuLVkBzkWEaWzqqsqM8f98cU',
        merkleRoot=generateHash(transactions)
    )

    blockHash = generateHash(header)

    return Block(
        hash=blockHash,
        header=header,
        transactions=transactions
    )


genesisBlock: Block = createGenesisBlock()
blockchain: Blockchain = [genesisBlock]


def getBlockchain() -> Blockchain:
    return blockchain


def getHead() -> Block:
    return blockchain[len(blockchain) - 1]


def createNewBlock(transactions) -> Block:
    head = getHead()

    header = BlockHeader(
        level=head['header']['level'] + 1,
        previousHash=head['hash'],
        timestamp=getTimestamp(),
        miner=myKey['pkh'],
        merkleRoot=generateHash(transactions)
    )

    blockHash = generateHash(header)

    return Block(
        hash=blockHash,
        header=header,
        transactions=transactions
    )


def pushBlock(block: Block):
    getBlockchain().append(block)


if __name__ == "__main__":
    print(json.dumps(blockchain, indent=2))
