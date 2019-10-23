import asyncio
import websockets
import time

#async def hello():
#    uri = "ws://localhost:8025/test"
#    while True:
#        async with websockets.connect(uri) as websocket:
#            msg = input("> ")
#            
#            await websocket.send(msg)
#
#            recieved = await websocket.recv()
#            print(recieved)

async def producer():
    time.sleep(0.01)
    return str(time.time())

async def consumer(val):
    print(val)

async def handler(websocket):
    consumer_task = asyncio.ensure_future(consumer_handler(websocket))
    producer_task = asyncio.ensure_future(producer_handler(websocket))

    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)

async def producer_handler(websocket):
    while True:
        message = await producer()
        await websocket.send(message)

def setup():
    uri = "ws://localhost:8025/test"
    asyncio.run(main(uri))

async def main(uri):
    async with websockets.connect(uri) as websocket:
        await handler(websocket)


if __name__ == "__main__":
    setup()