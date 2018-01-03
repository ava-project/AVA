""""
    Here is the MobileInput class who handles phone microphone interactions
    through the AVA mobile application
"""

import io
import sys
import wave
import asyncio
import websockets
from ctypes import *
import pyaudio

class MobileInput:
    def __init__(self, queues):
        self.input_queues = queues
        self.audio = pyaudioPyAudio()
        self.listening = True

    def __del__(self):
        self.audio.terminate()

    def write_to_file(self, all_datas):
        audio_file = io.BytesIO()
        wf = wave.Wave_write(audio_file)
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b''.join(all_datas))
        audio_file.seek(0)
        self.input_queue.put(audio_file)

    def run(self):
        try:
            stream = self.audio.open(format=pyaudio.paInt16,
                                     channels=2,
                                     rate=44100,
                                     input=True,
                                     frames_per_buffer=2048)

            while self.listening == True:
                all_datas = []
                data = stream.read(2048)
                all_datas.append(data)
                write_to_file(self, all_datas)
        except:
            print ("Error while reading on Microphone")
        stream.close()

    def stop(self):
        self.listening = False
