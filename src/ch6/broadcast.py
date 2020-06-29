import asyncio


def broadcast(message):
    from .socket import getPeers, createMessage

    async def send():
        print(f"[=>*] Broadcasting to peers", getPeers())
        for (_, sock) in getPeers().items():
            await sock.send(message)

    asyncio.ensure_future(send())

def broadcastBlock(block):
    from .socket import createMessage

    broadcast(
        createMessage(
            'BlockInjected',
            block))


def broadcastTx(tx):
    from .socket import createMessage

    broadcast(
        createMessage(
            'TransactionInjected',
            tx))
