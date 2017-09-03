import websockets
import asyncio

class STT_Engine_WebSocket():

    async def recognize(self, stream, queue_manager):
        async with websockets.connect('ws://172.17.0.2:8766') as websocket:
            print("Connecting to AVA Servers with address 172.17.0.2:8766")
            print("Sending file to server..")
            await websocket.send(b''.join(stream))
            print("Receiving sentence..")
            message = await websocket.recv()
            print(message)
            try:
                if message:
                    queue_manager.queue_command.put(message)
                    queue_manager.queue_input.task_done()
                    queue_manager.queue_tts.put("Okay")
            except:
                queue_manager.queue_tts.put("Retry your command please")
