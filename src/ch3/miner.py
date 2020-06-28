from customTypes.block import Block, BlockHeader
from blockchain import blockchain
from crypto import sha256_raw

# 블록헤더 + nonce를 가지고 difficulty target 이하의 값을 찾는
# 해시를 만든다

difficultyPeriod = 10
maxDifficulty = 0xffff * 256 ** (0x1d - 3)


def mine(header: BlockHeader):
    #
    header.difficulty = calculateDifficulty(header)

    # initial value
    nonce = 0
    blockHash = f""

    target = maxDifficulty / header.difficulty

    while True:
        header.nonce = nonce
        blockHash = sha256_raw(header)

        if blockHash < target then:
            break

        nonce = nonce + 1

    # found header
    return (blockHash, header)


def calculateDifficulty(header: BlockHeader):
    #     const {level, timestamp} = nextBlockHeader
    #     const blockchain = getBlockchain()

    # if ((level % DIFFICULTY_PERIOD) !== 0) return
    # getHead().header.difficulty

    #     const lastCalculatedBlock = blockchain[level - DIFFICULTY_PERIOD]
    #     const lastCalculatedDifficulty = lastCalculatedBlock.header.difficulty

    #     const previousTarget = difficultyConstant / lastCalculatedDifficulty
    #     const timeDifference = timestamp - lastCalculatedBlock.header.timestamp
    #     const timeExpected = BLOCK_INTERVAL * DIFFICULTY_PERIOD

    #     const nextTarget = previousTarget * timeDifference / timeExpected
    #     const nextDifficulty = difficultyConstant / nextTarget

    #     return nextDifficulty

    level = header.level
    timestamp = header.timestamp
    lastCalculatedBlock = blockchain[level - difficultyPeriod]
    lastCalculatedDifficulty = lastCalculatedBlock.difficulty

    previousTarget = maxDifficulty / lastCalculatedDifficulty
    timeDifference =

    return header.difficulty


# import {
#     BLOCK_INTERVAL,
#     DIFFICULTY_PERIOD
# } from './constants.json'
# import {Block} from './types/block'
# import {getBlockchain
#         import calculateBlockHash
#         import getHead} from './blockchain'
# import BN from 'bn.js'

# interface MineResult {
#     hash: string,
#     header: Block["header"]
# }

# const difficultyConstant = 0xffff * 256 ** (0x1d - 3)

# export const mine = (nextBlockHeader: Block["header"]): MineResult = > {

#     // should change difficulty?
#     const difficulty = calculateDifficulty(nextBlockHeader)
#     const target = BigInt(difficultyConstant / difficulty)

#     nextBlockHeader.difficulty = difficulty

#     let nonce = 0
#     let blockHash: string = ''

#     while(true) {
#         nextBlockHeader.nonce = nonce
#         blockHash = calculateBlockHash(nextBlockHeader)

#         // console.log({blockHash})
#         // console.log({difficulty})
#         // process.stdout.write(`\r${BigInt(`0x${blockHash}`)}`)
#         // console.log(new BN(blockHash))
#         // console.log(new BN(target.toString()))
#         if(BigInt(`0x${blockHash}`) < BigInt(target)) break

#         nonce + +
#     }

#     console.log('block created', {
#         level: nextBlockHeader.level,
#         difficulty: nextBlockHeader.difficulty,
#         nonce,
#         hash__: BigInt(`0x${blockHash}`),
#         target: target
#     })

#     return {
#         hash: blockHash,
#         header: nextBlockHeader
#     }
# }

# const calculateDifficulty = (nextBlockHeader: Block["header"]) = > {
#     const {level, timestamp} = nextBlockHeader
#     const blockchain = getBlockchain()

#     if ((level % DIFFICULTY_PERIOD) !== 0) return getHead().header.difficulty

#     const lastCalculatedBlock = blockchain[level - DIFFICULTY_PERIOD]
#     const lastCalculatedDifficulty = lastCalculatedBlock.header.difficulty

#     const previousTarget = difficultyConstant / lastCalculatedDifficulty
#     const timeDifference = timestamp - lastCalculatedBlock.header.timestamp
#     const timeExpected = BLOCK_INTERVAL * DIFFICULTY_PERIOD

#     const nextTarget = previousTarget * timeDifference / timeExpected
#     const nextDifficulty = difficultyConstant / nextTarget

#     return nextDifficulty
# }
