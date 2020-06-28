from customTypes.transaction import TxIn, TxOut, Transaction, blockReward
from crypto import sha256, signTx
import json


def createCoinbaseTx(myKey, blockLevel):
    txIn = TxIn(
        txOutId="0",
        txOutIdx=blockLevel
    )
    txIns = [txIn]

    txOut = TxOut(
        address=myKey,
        amount=blockReward
    )
    txOuts = [txOut]
    txId = sha256(json.dumps([txIns, txOuts]))

    return Transaction(
        txIns=txIns,
        txOuts=txOuts,
        txId=txId,
        signature=signTx(txId)
    )
