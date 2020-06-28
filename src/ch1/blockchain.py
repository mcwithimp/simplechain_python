import json
import os
import sys
import time
from .customTypes.block import Block, BlockHeader, Blockchain
from ..lib.crypto import getKeys, sha256


def generateHash(data: object) -> str:
    return sha256(json.dumps(data))


myKey = getKeys('ada')
"""
 "alias": "ada",
 "sk": "fc487a5adcb6fe82ac8de12f2c6cffa2b395bae0b694591c1a9ef973552e4030",
 "pk": "c621e37b2be6e83ce77b539a90f6fc99a218986499a5b7565283eb9ec369f5c08f527af268fa9a274613804f8773b042e1866a84c705ddc18bb6f05598d7456a",
 "pkh": "1G8RdTC6nSmuLVkBzkWEaWzqqsqM8f98cU"
"""


def createGenesisBlock() -> Block:
    transactions = ['Alice sends 10 btc to Bob']
    header = BlockHeader(
        level=0,
        previousHash='0' * 64,
        timestamp=1_593_332_227,
        miner='1G8RdTC6nSmuLVkBzkWEaWzqqsqM8f98cU',
        merkleRoot=generateHash(transactions)
    )

    return Block(
        header=header,
        transactions=transactions
    )


genesisBlock: Block = createGenesisBlock()
blockchain: Blockchain = [genesisBlock]

print(json.dumps(blockchain, indent=2))


def createBlock(level, previousHash, timestamp,
                miner, nonce, difficulty, merkleRoot):
    pass


# def header(self, nonce=None) -> str:
#     """
#     This is hashed in an attempt to discover a nonce under the difficulty
#     target.
#     """
#     return (
#         f'{self.version}{self.prev_block_hash}{self.merkle_hash}'
#         f'{self.timestamp}{self.bits}{nonce or self.nonce}')

# @property
# def id(self) -> str: return sha256d(self.header())
