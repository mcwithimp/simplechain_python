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

    blockHash = generateHash(header)

    return Block(
        hash=blockHash,
        header=header,
        transactions=transactions
    )


genesisBlock: Block = createGenesisBlock()
blockchain: Blockchain = [genesisBlock]


def getBlockchain() -> Blockchain:
    return blockchain


def getHead() -> Block:
    return blockchain[len(blockchain) - 1]


def getTimestamp() -> int:
    return int(time.time())


def createNewBlock(transactions) -> Block:
    head = getHead()

    header = BlockHeader(
        level=head['header']['level'] + 1,
        previousHash=head['hash'],
        timestamp=getTimestamp(),
        miner=myKey['pkh'],
        merkleRoot=generateHash(transactions)
    )

    blockHash = generateHash(header)

    return Block(
        hash=blockHash,
        header=header,
        transactions=transactions
    )


def pushBlock(block: Block):
    getBlockchain().append(block)


if __name__ == "__main__":
    print(json.dumps(blockchain, indent=2))
