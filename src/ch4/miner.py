from ..lib.crypto import sha256, generateHash
import json
import threading

# 마이닝 쓰레드 이벤트 핸들러
minerInterrupt = threading.Event()

# 블록헤더 + nonce를 가지고 difficulty target 이하의 값을 찾는
# 해시를 만든다

difficultyConstant = 0xffff * 256 ** (0x1d - 3)
PARAMS_PATH = "src/parameters.json"
with open(PARAMS_PATH, 'r') as params_file:
    params = json.load(params_file)


def mine(header, blockchain):
    # 마이닝 쓰레드 초기화
    minerInterrupt.clear()

    # 이번 블럭의 타겟 난이도 계산
    header["difficulty"] = calculateDifficulty(header, blockchain)

    # initial value
    nonce = 0
    blockHash = ""

    target = difficultyConstant / header["difficulty"]

    while True:
        # 마이닝중에 다른 블록이 찾아지면 (다른 노드가 블록을 먼저 찾으면)
        # 마이너를 중단시킨다.
        if minerInterrupt.is_set():
            minerInterrupt.clear()
            return None

        header["nonce"] = nonce
        blockHash = generateHash(header)

        if (int(blockHash, base=16) < target):
            break

        nonce = nonce + 1

    # found header
    return {
        "blockHash": blockHash,
        "header": header
    }


def calculateDifficulty(header, blockchain) -> int:
    level = header["level"]
    timestamp = header["timestamp"]

    if ((level % params["DIFFICULTY_PERIOD"]) != 0):
        return header["difficulty"]

    lastCalculatedBlock = blockchain[level - params["DIFFICULTY_PERIOD"]]
    lastCalculatedDifficulty = lastCalculatedBlock["header"]["difficulty"]

    previousTarget = (difficultyConstant / lastCalculatedDifficulty)
    timeDifference = timestamp - lastCalculatedBlock["header"]["timestamp"]
    timeExpected = params["BLOCK_INTERVAL"] * params["DIFFICULTY_PERIOD"]

    nextTarget = previousTarget * timeDifference / timeExpected
    nextDifficulty = difficultyConstant / nextTarget

    return nextDifficulty


if __name__ == '__main__':
    testThread = threading.Event()
    header = {
        "level": 12,
        "timestamp": 1593353574,
        "difficulty": 0.00000035,
        "nonce": 0
    }

    print(mine(header, [], testThread))
