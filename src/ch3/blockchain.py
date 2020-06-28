import sys
from .customTypes.block import Block, BlockHeader, pushBlock
from .transaction import createCoinbaseTx
from .utxo import UTxOContext, updateUTxOContext


def createBlock(level, previousHash, timestamp,
                miner, nonce, difficulty, merkleRoot):
    pass


def initGenesis():
    genesisTx = createCoinbaseTx(sk="AAA", pk="BBB", blockLevel=1)
    block = Block(
        header=BlockHeader(
            level=1,
            previousHash=f'prevHash',
            timestamp=123,
            miner=f'me',
            nonce=123,
            difficulty=123,
            merkleRoot=f'merkleRoot'
        ),
        transactions=[
            # miner가 없으므로 아직은 myKey 없음
            # 일단 진행!
            genesisTx
        ]
    )

    # housekeeping
    updateUTxOContext(1, block)
    pushBlock(block)

    print(block, UTxOContext)


initGenesis()

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
