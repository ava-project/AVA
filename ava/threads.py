import threading

from .audio_input import AudioInput


class ThreadAudioInput(threading.Thread):

    def __init__(self):
        super().__init__()
        self.process = None
