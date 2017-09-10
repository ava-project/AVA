import websockets
import asyncio
import pickle
import base64

# Class connecting to ava_server with websocket, sending audio data
class STT_Engine_WebSocket():

    async def recognize(self, stream, queue_manager):
        async with websockets.connect("ws://172.17.0.2:8766") as ws:
            print("Connecting to AVA Servers with address ws://172.17.0.2:8766")
            print("Sending file to server..")
            binary = stream.read()
            b64_data = base64.b64encode(binary)
            await ws.send(binary)
            print("Receiving sentence..")
            message = await ws.recv()
            print(message)
            ws.close()
            try:
                if message:
                    queue_manager.queue_command.put(message)
                    queue_manager.queue_input.task_done()
                    queue_manager.queue_tts.put("Okay")
            except:
                queue_manager.queue_tts.put("Retry your command please")
