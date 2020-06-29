import websockets
import asyncio


def handler(websocket, path):
    while True:
        print(websocket.remote_address)


def websocket_test():
    return websockets.serve(handler, "0.0.0.0", 6767)


if __name__ == '__main__':
    eventloop = asyncio.get_event_loop()

    ws = websocket_test()

    websockets.connect('ws://localhost:6767')
    eventloop.run_until_complete(ws)
    eventloop.run_forever()
