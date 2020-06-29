import asyncio
import websockets

loop = asyncio.get_event_loop()

def websocketServerTask():
    async def handler(websocket, path):
        while True:
            print("what")
            data = await websocket.recv()
            await websocket.send("...")
            print(data)

    return websockets.serve(handler, "localhost", 8761)

async def sayWhatever():
    while True:
        print("k")
        await asyncio.sleep(1)

async def websocketClientTask():
    await asyncio.sleep(2)
    conn = await websockets.connect('ws://localhost:8761')

    while True:
        await conn.send("hi")
        await asyncio.sleep(1)
        data = await conn.recv()
        print(data)

async def main():
    t1 = sayWhatever()
    t2 = websocketServerTask()
    t3 = websocketClientTask()

    await asyncio.gather(
        t1,t2,t3
    )

asyncio.run(main())