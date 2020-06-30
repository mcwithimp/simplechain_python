from typing import Iterable
from .broadcast import broadcastTx
from .transaction import Transaction

mempool: Iterable[Transaction] = []

def getMempool():
    return mempool

def insertToMempool(tx):
    global mempool
    mempool.append(tx)

def removeFromMempool(tx):
    global mempool
    filtered = list(filter(lambda txInMempool: txInMempool["txId"] != tx["txId"], mempool))
    mempool = filtered
