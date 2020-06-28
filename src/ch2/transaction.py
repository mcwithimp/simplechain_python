import json
from typing import Iterable, TypedDict
from ..lib.crypto import sha256, signTransaction

PARAMS_PATH = "src/parameters.json"
with open(PARAMS_PATH, 'r') as params_file:
    params = json.load(params_file)


class TxIn(TypedDict):
    txOutId: str
    txOutIdx: str


class TxOut(TypedDict):
    amount: int
    address: str  # publickey_hash


class Transaction(TypedDict):
    # tx별 operation id
    txId: str

    # tx 생성자가 sk로 sign한 signature
    signature: str

    txIns: Iterable[TxIn]
    txOuts: Iterable[TxOut]


def createCoinbaseTx(pk: str, sk: str, level: int):
    txIn = TxIn(
        txOutId="00",
        txOutIdx=level
    )
    txIns = [txIn]

    txOut = TxOut(
        address=pk,
        amount=params['BLOCK_REWARD']
    )
    txOuts = [txOut]
    txId = sha256(json.dumps([txIns, txOuts]))

    return Transaction(
        txIns=txIns,
        txOuts=txOuts,
        txId=txId,
        signature=signTransaction(sk, txId)
    )
