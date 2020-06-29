from typing import Iterable
from .transaction import Transaction

mempool: Iterable[Transaction] = []

def getMempool():
    return mempool

def insertToMempool(tx):
    global mempool
    mempool.append(tx)