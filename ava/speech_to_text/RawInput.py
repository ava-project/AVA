""""
    Here is the RawInput class who handles computer microphone interactions
"""

from ctypes import *
import pyaudio

RATE = 44100
FPB = 2048
CHUNK = 1024


class RawInput:

    def __init__(self):
        """
        Initiate audio ports with PyAudio instance
        """
        # Define our error handler type for ALSA
        ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
        def py_error_handler(filename, line, function, err, fmt):
            pass
        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
        asound = cdll.LoadLibrary('libasound.so')
        # Set error handler
        asound.snd_lib_error_set_handler(c_error_handler)

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(input_device_index=0, format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=FPB)

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
