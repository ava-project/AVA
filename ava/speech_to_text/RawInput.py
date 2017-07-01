""""
    Here is the RawInput class who handles computer microphone interactions
"""

import pyaudio

RATE = 16000
FPB = 2048
CHUNK = 1024


class RawInput:

    def __init__(self):
        """
        Initiate audio ports with PyAudio instance
        """
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=FPB)

    def __del__(self):
        """
        Destroy the instance of PyAudio
        """
        self.audio.terminate()

    def start(self):
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()

    def read(self):
        buff = self.stream.read(CHUNK)
        return buff
