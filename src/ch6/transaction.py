import json
from typing import Iterable, TypedDict
from .utxo import getUTxOContext
from ..lib.crypto import sha256, signTransaction
from functools import reduce

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
        txOutId='0' * 64,
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

def sortByAmount(utxo):
    return utxo["amount"]

def transfer(fr, to, amt):
    keys = "src/keys.json"
    with open(keys, 'r') as key_file:
        keys = json.load(key_file)
        myKey = [key for key in keys if key["alias"] == fr][0]
        unspentUtxo = []

        headUtxo = getUTxOContext()[-1]

        for (_, key) in enumerate(headUtxo):
            utxo = headUtxo[key]
            if utxo["address"] == myKey["pk"]:
                unspentUtxo.append(utxo)
                
        unspentUtxo.sort(key=sortByAmount)
        balance = reduce(lambda acc,utxo: acc + utxo["amount"], unspentUtxo, 0)

        if balance < int(amt,10):
            print('not enough balance')
            return

        totalAmount = int(amt, 10)
        toSpend = []
    
        while totalAmount > 0:
            utxo = unspentUtxo.pop(0)
            totalAmount = totalAmount - utxo["amount"]
            toSpend.append(utxo)

        changeToMe = totalAmount * -1

        txIns = []
        for spendingUtxo in toSpend:
            txIns.append(TxIn(
                txOutId=spendingUtxo["txOutId"],
                txOutIdx=spendingUtxo["txOutIdx"]
            ))

        txOuts = [
            TxOut(
                address=[key for key in keys if key["alias"] == to][0]["pk"],
                amount=int(amt,10)
            )
        ]

        if changeToMe != 0:
            txOuts.append(TxOut(
                address=myKey["pk"],
                amount=changeToMe
            ))

        txId = sha256(json.dumps([txIns, txOuts]))
        signature = signTransaction(myKey["sk"], txId)

        return Transaction(
            txId=txId,
            txIns=txIns,
            txOuts=txOuts,
            signature=signature
        )

if __name__ == '__main__':
    with open('src/keys.json', 'r') as key:
        keys = json.load(key)
        mc = keys[0]
        transfer("mc", "multicampus1", 200)
