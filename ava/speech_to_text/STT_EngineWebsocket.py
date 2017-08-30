from websocket import create_connection

class STT_Engine_WebSocket():

    def __init__(self):
        self.ws = create_connection("ws://192.168.1.30:8765")

    def recognize(self, stream):
        print("Sending file to server..")
        self.ws.send(stream)
        print("Receiving sentence..")
        return self.ws.recv()

    def __del__(self):
        self.ws.close()
