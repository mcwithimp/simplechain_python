from .blockchain import getBlockchain
from .mempool import getMempool
from .utxo import getHeadUTxOContext
from ..lib.crypto import generateHash, verifyTxSignature
from .miner import difficultyConstant
import json

PARAMS_PATH = "src/parameters.json"
with open(PARAMS_PATH, 'r') as params_file:
    params = json.load(params_file)

BLOCK_INTERVAL = params['BLOCK_INTERVAL']


# 비트코인 위키 참고
# 블록의 타임 스탬프는 아래와 조건을 만족해야 한다.
# if it is greater than the median timestamp of previous 11 blocks,
# and less than the network - adjusted time + 2 hours. (2 hours = 12 times BLOCK_INTERVAL)
# Adjusting time is because of asynchronous time between processes
def verifyTimestamp(previousTime: int, newTime: int) -> bool:
    lowerBound = previousTime - (BLOCK_INTERVAL * 6)
    upperBound = previousTime + (BLOCK_INTERVAL * 12)
    return (lowerBound <= newTime and newTime <= upperBound)


def verifyBlock(block) -> bool:
    header = block['header']
    # 블록 해시가 올바르게 계산되었는지 확인한다.
    if (generateHash(block['transactions']) != header['merkleRoot']):
        print("merkleRoot is not valid!")
        return False
    elif (generateHash(header) != block['hash']):
        print("blockHash is not valid!")
        return False

    # 작업 증명을 확인한다.
    difficulty = header['difficulty']
    target = difficultyConstant / difficulty

    if (int(block['hash'], 16) >= target):
        print("PoW is not valid!")
        return False

    return True


def verifyChain(candidateChain) -> bool:
    # 피어에게 블록체인을 받은 경우 == 피어의 블록체인이 나의 블록체인보다 더 긴 경우에만 체인을 검증한다
    localChain = getBlockchain()
    localGenesisBlock = localChain[0]
    remoteGenesisBlock = candidateChain[0]

    # (피어로부터 받은) 체인이 제네시스 블록을 가지고 있는지 확인한다.
    if (remoteGenesisBlock['header']['level'] != 0
            or remoteGenesisBlock == localGenesisBlock):
        print('The remote genesis block is invalid!')
        return False

    # 각 블록들을 검증하고, 체인이 올바르게 이어져 있는지 확인한다.
    for i in range(1, len(candidateChain)):
        currentBlock = candidateChain[i]
        previousBlock = candidateChain[i - 1]
        if (currentBlock['header']['level'] !=
                previousBlock['header']['level'] + 1):
            print("Block level is not valid!")
            return False
        elif (currentBlock['header']['previousHash'] != previousBlock['hash']):
            print("Previous hash is not valid!")
            return False
        # elif (verifyTimestamp(previousBlock['header']['timestamp'], currentBlock['header']['timestamp']) == False):
        #     print("Timestamp value is not valid!")
        #     return False
        elif (verifyBlock(currentBlock) == False):
            return False

        return True


def verifyTxIns(txIns, headContext, txId, signature) -> bool:
    for txIn in txIns:
        target = f"{txIn['txOutId']}_{txIn['txOutIdx']}"
        isUnspent = headContext.hasOwnProperty(target)

        if (isUnspent == False):
            print("Claimed utxo doesn't exist!")
            return False

        pkh = headContext[target]['address']
        if (verifyTxSignature(txId, signature, pkh) == False):
            print("Tx's signature is not valid!")
            return False

    return True


def isTxInDoubledClaimed(candidateTx) -> bool:
    mempool = getMempool()

    for txInMempool in mempool:
        for txIn in txInMempool['txIns']:
            for candiTxIn in candidateTx['txIns']:
                if(candiTxIn['txOutId'] == txIn['txOutId'] and
                   candiTxIn['txOutIdx'] == txIn['txOutIdx']):
                    return True

    return False


def verifyTx(tx) -> bool:
    headContext = getHeadUTxOContext()

    if (isTxInDoubledClaimed(tx) == True):
        print("One of TxIns is doubly claimed!")
        return False

    if (generateHash({tx['txIns'], tx['txOuts']}) != tx['txId']):
        print("TxId is not valid!")
        return False
    elif (verifyTxIns(tx['txIns'], headContext, tx['txId'], tx['signature']) == False):
        print("Claim of txIns is not valid!")
        return False

    txInsAmount = 0
    for txIn in tx['txIns']:
        amount = headContext[f"{txIn['txOutId']}_{txIn['txOueIdx']}"]['amount']
        txInsAmount += amount

    txOutsAmount = 0
    for txOut in tx['txOuts']:
        txOutsAmount += txOut['amount']

    if (txInsAmount != txOutsAmount):
        print("TxIns' amount is different with TxOuts' amount!")
        return False

    return True
