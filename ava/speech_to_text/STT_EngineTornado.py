import websocket

import json
import functools
import base64

APPLICATION_JSON = 'application/json'

class STT_Engine_Tornado():
    def __init__(self):
        self.tornado_connection = None

    def connect(self, server_url):
        websocket.enableTrace(True)
        self.tornado_connection = websocket.create_connection(server_url)

    def recognize(self, stream, queue_manager):
        binary = stream.read()
        b64_data = base64.b64encode(binary)
        self.tornado_connection.send(binary)
        print("Receiving sentence..")
        result = self.tornado_connection.recv()
        print(result)
