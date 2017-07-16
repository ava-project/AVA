import time
import os

from tempfile import NamedTemporaryFile
from sys import platform as _platform

from gtts import gTTS

from .playsound import playsound
from ..queues import QueueTtS
from ..components import _BaseComponent


class TextToSpeech(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_tts = QueueTtS()

    def run(self):
        sentence = self.queue_tts.get()
        print('To say out loud : {}'.format(sentence))
        tts = gTTS(text=sentence, lang='en')
        if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
            with NamedTemporaryFile() as audio_file:
                tts.write_to_fp(audio_file)
                audio_file.seek(0)
                playsound(audio_file.name)
        else:
            filename = str(time.time()).split('.')[0] + ".mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        self.queue_tts.task_done()
