""""
    Here is the RawInput class who handles computer microphone interactions
"""

from ctypes import *
import pyaudio

# RATE = 44100
# FPB = 2048
# CHUNK = 1024


class RawInput:

    def __init__(self):
        """
        Initiate audio ports with PyAudio instance
        """
        # Define our error handler type for ALSA
        # ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
        # def py_error_handler(filename, line, function, err, fmt):
        #     pass
        # c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
        # asound = cdll.LoadLibrary('libasound.so')
        # Set error handler
        # asound.snd_lib_error_set_handler(c_error_handler)
        self.record = []
        self.done = False
        self.listening = True
        self.audio = pyaudio.PyAudio()

    def __del__(self):
        """
        Destroy the instance of PyAudio
        """
        self.audio.terminate()

    #Setting reading variables to start/stop vocal recording
    def start(self):
        self.record = []
        self.done = False
        self.listening = True

    def stop(self):
        self.listening = False

    # Reading vocal entry
    def read(self):
        self.start()
        stream = self.audio.open(format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=2048)
        while self.listening:
            data = stream.read(2048)
            self.record.append(data)
        stream.close()
        self.done = True
