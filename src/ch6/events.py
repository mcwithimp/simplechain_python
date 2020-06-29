import json
from typing import TypedDict
from


"""
possible message
    'PEER_REQUEST',
    'PEER_RESPONSE',
    'SYNC_REQUEST',
    'SYNC_RESPONSE',
    'BLOCK_INJECTED',
    'TRANSACTION_INJECTED',
    'MEMPOOL_REQUEST',
    'MEMPOOL_RESPONSE'
"""


class Message(TypedDict):
    msgType: str
    payload: object


def createPeerRequestMsg(ip: string, port: number):
    return json.dumps({
        msgType: 'PEER_REQUEST',
        body: {ip, port}
    })


def createPeerResponseMsg(peers):
    return json.dumps({
        msgType: 'PEER_RESPONSE',
        body: peers
    })


def createSyncRequestMsg(remoteHeader):
    return json.dumps({
        msgType: 'SYNC_REQUEST',
        body: remoteHeader
    })


def createSyncResponseMsg(blockchain):
    return json.dumps({
        msgType: 'SYNC_RESPONSE',
        body: blockchain
    })


'BLOCK_INJECTED',
    'TRANSACTION_INJECTED',
    'MEMPOOL_REQUEST',
    'MEMPOOL_RESPONSE


def createBlockInjectedMsg(block):
    return json.dumps({
        msgType: 'BLOCK_INJECTED',
        body: block
    })


def createMessage(msgType, payload):
    return Message(
        msgType=msgType,
        payload=payload
    )


async def handler(websocket, path):
    payload = await websocket.recv()
    msg: Message = json.loads(payload)
    msgType = msg['msgType']

    if msgType == 'PeerRequest':
        response = createMessage('PeerResponse', json.dumps(peers))
        pass
    elif msgType == 'PeerResponse':
        pass
    elif msgType == 'SyncRequest':
        pass
    elif msgType == 'SyncResponse':
        pass
    elif msgType == 'BlockInjected':
        pass
    elif msgType == 'TransactionInjected':
        pass
    elif msgType == 'MempoolRequest':
        pass
    elif msgType == 'MempoolResponse':
        pass
    else:
        print("Oops")
    