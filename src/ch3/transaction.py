from .customTypes.transaction import TxIn, TxOut, Transaction, blockReward
from ..lib.crypto import sha256, signTransaction
import json


def createCoinbaseTx(pk: str, sk: str, blockLevel):
    txIn = TxIn(
        txOutId="0",
        txOutIdx=blockLevel
    )
    txIns = [txIn]

    txOut = TxOut(
        address=pk,
        amount=blockReward
    )
    txOuts = [txOut]
    txId = sha256(json.dumps([txIns, txOuts]))

    return Transaction(
        txIns=txIns,
        txOuts=txOuts,
        txId=txId,
        signature=signTransaction(sk, txId)
    )
