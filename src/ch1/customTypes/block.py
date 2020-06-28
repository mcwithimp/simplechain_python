from typing import Iterable, NamedTuple, TypedDict

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


Blockchain: Iterable[Block] = []
