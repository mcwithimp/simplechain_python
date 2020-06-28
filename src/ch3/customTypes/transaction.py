from typing import Iterable, NamedTuple

blockReward = 10


class TxIn(NamedTuple):
    txOutId: str
    txOutIdx: str


class TxOut(NamedTuple):
    amount: int
    address: str  # publickey


class Transaction(NamedTuple):
    # tx별 operation id
    txId: str

    # tx 생성자가 pk로 sign한 signature
    signature: str

    txIns: Iterable[TxIn]
    txOuts: Iterable[TxOut]
