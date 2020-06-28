import hashlib
import ecdsa
import json
from customTypes.transaction import Transaction
from base58 import b58encode_check


def sha256(payload):
    sha = hashlib.sha256(payload.encode('utf8')).digest()
    ripe = hashlib.new('ripemd160', sha).digest()
    return b58encode_check(b'\x00' + ripe)

# TODO: impelement me


def signTx(tx: str):
    return tx
