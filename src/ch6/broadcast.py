

def broadcast(message):
    from .socket import peers, createMessage
    print("[=>*] Broadcasting ...")
    for (_, sock) in peers.items():
        sock.send(message)
    print("[=>*] ============ Broadcasting")


def broadcastBlock(block):
    from .socket import peers, createMessage

    broadcast(createMessage('BlockInjected', block))


def broadcastTx(tx):
    from .socket import peers, createMessage

    broadcast(createMessage('TransactionInjected', tx))
