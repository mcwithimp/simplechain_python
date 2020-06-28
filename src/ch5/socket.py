import json
import websockets
from .blockchain import getHead, getBlockchain, replaceChain, pushBlock
from .verifier import verifyChain
from .miner import minerInterrupt
from .utxo import updateUTxOContext
from typing import TypedDict, Iterable, Dict


"""
possible message
    'PeerRequest',
    'PeerResponse',
    'SyncRequest',
    'SyncResponse',
    'BlockInjected',
    'TransactionInjected',
    'MempoolRequest',
    'MempoolResponse'
"""

peers = {}


async def handler(websocket, path):
    global peers
    payload = await websocket.recv()
    msg = json.loads(payload)
    msgType = msg['msgType']
    body = json.loads(msg['body'])

    print(f"Received Message {msgType} from {websocket.remote_address[0]}")

    if msgType == 'PeerRequest':
        await websocket.send(createMessage('PeerResponse', list(peers)))
        peers[websocket.remote_address[0]] = websocket

    elif msgType == 'PeerResponse':
        peers = body
        for peer in peers:
            peers[peer] = await websockets.connect(peer)

    elif msgType == 'SyncRequest':
        localHeader = getHead()['header']
        remoteHeader = body

        print("SyncRequest", localHeader, remoteHeader)

        # 상대방 블록이 내거보다 높으면 싱크 리퀘스트를 보낸다
        if remoteHeader["level"] > localHeader["level"]:
            await websocket.send(createMessage('SyncRequest', localHeader))

        # 레벨이 같으면 아무것도 하지 않는다 (경합상황)
        elif remoteHeader["level"] == localHeader["level"]:
            await websocket.send(createMessage('SyncResponse', None))

        # 내 blockheight가 더 높다.
        else:
            await websocket.send(createMessage('SyncResponse', getBlockchain()))

    elif msgType == 'SyncResponse':
        remoteBlockchain = body

        # 상대 피어와 체인 레벨이 같은 경우
        if remoteBlockchain is None:
            return

        # 상대 피어의 체인 레벨이 높은 경우
        # 간단한 verify 진행 후 블록체인을 replace한다.
        if verifyChain(remoteBlockchain) is True:
            replaceChain(remoteBlockchain)

    # 블록이 Inject 된 경우, 채굴을 잠시 멈추고 Block을 push 한 뒤
    # 다시 채굴 시작
    elif msgType == 'BlockInjected':
        localHead = getHead()

        # 만약 받아온 블럭이 내가 가진 블록체인의 latest block보다
        # 2 이상 height 차이가 난다면 싱크가 많이 벌어졌으므로
        # SyncRequest를 보낸다.
        if body["header"]["level"] > localHead["header"]["level"] + 1:
            await websocket.send(createMessage('SyncRequest', localHead["header"]))
            minerInterrupt.set()
            return

        # 만약 받아온 블록의 level이 나의 최신 block의 레벨보다 작거나 같다면
        # 아무것도 하지 않는다 (내 체인이 더 길거나 경합상황)
        elif body["header"]["level"] <= localHead["header"]["level"]:
            pass

        # 받아온 블록을 현재 블록체인에 붙여보고,
        # 만약 verify에 통과하지 못한다면 에러메시지를 띄우고
        # 핸들러를 종료한다
        elif verifyChain([body]) is False:
            print("Injected block is not valid")
            pass

        # 여기까지 왔다면 모든 verification을 통과한 것
        # block을 push하면서, UTxOSet을 업데이트 한다.
        # 이 때, Injected 된 블록의 Tx에서 이미 사용된 UTxO (새 블록의 txIns)는
        # 로컬 UTxOContext 에서 삭제해야 한다. (updateUTxOContext 변경)
        pushBlock(body)
        updateUTxOContext(level=body["header"]["level"], block=body)

    elif msgType == 'TransactionInjected':
        pass
    elif msgType == 'MempoolRequest':
        pass
    elif msgType == 'MempoolResponse':
        pass
    else:
        print("Oops")


class Message(TypedDict):
    msgType: str
    body: object


def createMessage(msgType: str, data: object):
    print(f"creating message {msgType}")
    return Message(msgType=msgType, body=json.dumps(data))
