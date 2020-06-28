from typing import Iterable, NamedTuple
from .transaction import Transaction


class BlockHeader(NamedTuple):
    # 현재 블록의 레벨(=높이)
    level: int

    # 이전 블록의 해시
    previousHash: str

    # 현재 블록의 타임스탬프
    timestamp: int

    # 마이닝 정보
    # 1. 마이너: 비트코인에서는 코인베이스 트랜잭션으로 표기하고 별도의 miner 정보는 없음
    miner: str
    # 2. 논스: 블록 해시를 난이도 목표 이하로 만들기 위한 값
    nonce: int
    # 3. 난이도: 블록 해시는 (2 ** 256 >> difficulty) 이하여야 함
    difficulty: int

    # 머클 트리의 해시 (txsHash)
    merkleRoot: str


class Block(NamedTuple):
    # 블록 헤더
    header: BlockHeader

    # 트랜잭션
    transactions: Iterable[Transaction]


def pushBlock(block: Block):
    blockchain.append(block)


transactions: [Transaction]
blockchain: Iterable[Block] = []
