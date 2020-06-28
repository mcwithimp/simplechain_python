from typing import Iterable, NamedTuple


class UTxO(NamedTuple):
    txOutId: str
    txOutIdx: str
    address: str
    amount: int
