from typing import Iterable
from .transaction import Transaction

mempool: Iterable[Transaction] = []

def getMempool():
    return mempool
