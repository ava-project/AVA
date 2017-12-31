import websockets
import asyncio
import pickle
import base64

# Class connecting to ava_server with websocket, sending audio data
class STT_Engine_WebSocket():

    def __init__(self):
        self.watsonUrl = "wss://www.ava-project.com/ava_server"
        self.sphinxUrl = "wss://www.ava-project.com/shinx"
        self.currentUrl = self.watsonUrl

    def switchServer(self, toUrl):
        if toUrl == "watson":
            self.currentUrl = self.watsonUrl
        elif toUrl == "sphinx":
            self.currentUrl = selfsphinxUrl


    async def recognize(self, stream, queue_manager):
        async with websockets.connect(self.currentUrl) as ws:
            print("Connecting to AVA Servers with address ws://ava-project.com/ava_server")
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
