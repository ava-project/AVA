import io
import sys
import wave
import asyncio
import websockets
import socket

from ..queues import QueueInput
from ..components import _BaseComponent, RunOneTime


class MobileBridgeInput(RunOneTime, _BaseComponent):

    def __init__(self):
        super().__init__()
        self.input_queue = QueueInput()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def write_to_file(self, audio):
        audio_file = io.BytesIO()
        wf = wave.Wave_write(audio_file)
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(audio)
        audio_file.seek(0)
        print('inserting in input_queue')
        self.input_queue.put(audio_file)

    async def listener(self, websocket, path):
        try:
            audio = await websocket.recv()
            print('Audio from mobile deviced received')
            self.write_to_file(audio)
        except:
            pass

    def run(self):
        start_server = websockets.serve(self.listener, '0.0.0.0', 8765)
        print("Mobile Bridge listening on {}:8765".format(self.get_ip_address()))
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()
