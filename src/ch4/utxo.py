from typing import Iterable, TypedDict, Dict

"""types"""


class UTxO(TypedDict):
    txOutId: str
    txOutIdx: str
    address: str  # publickey_hash
    amount: int


UTxOSet = Dict[str, UTxO]
Context = Iterable[UTxOSet]

"""assignment"""
UTxOContext: Context = []


def getUTxOContext() -> Context:
    return UTxOContext


def updateUTxOContext(level: int, block):
    # 가장 최근의 UTxOContext를 가져온다.
    utxoContext = UTxOContext if len(UTxOContext) else {}

    transactions = block['transactions']
    for tx in transactions:
        for txOutIdx, txOut in enumerate(tx['txOuts']):
            utxo = UTxO(
                txOutId=tx['txId'],
                txOutIdx=txOutIdx,
                address=txOut['address'],
                amount=txOut['amount']
            )

            utxoContext["tx.txId_{idx}".format(idx=txOutIdx)] = utxo

    getUTxOContext().append(utxoContext)
