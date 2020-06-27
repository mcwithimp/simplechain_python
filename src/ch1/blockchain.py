import sys
from customTypes.block import Block, BlockHeader


def createBlock(level, previousHash, timestamp,
                miner, nonce, difficulty, merkleRoot):
    pass


block = Block(
    header=BlockHeader(
        level=1,
        previousHash='prevHash',
        timestamp=123,
        miner='me',
        nonce=123,
        difficulty=123,
        merkleRoot='merkleRoot'
    ),
    transactions=[]
)

print(block)
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
