import time
import os

from tempfile import NamedTemporaryFile
from sys import platform as _platform

from gtts import gTTS
from pygame import mixer

from .playsound import playsound
from ..components import _BaseComponent


class TextToSpeech(_BaseComponent):

    def __init__(self, queues):
        super().__init__(queues)
        self.queue_tts = None

    def setup(self):
        self.queue_tts = self._queues['QueueTextToSpeech']

    def run(self):
        while self._is_init:
            # sentence = self.queue_tts.get()
            # if sentence is None:
            #     break
            # print('To say out loud : {}'.format(sentence))
            # tts = gTTS(text=sentence, lang='en')
            # if _platform == "darwin":
            #     with NamedTemporaryFile() as audio_file:
            #         tts.write_to_fp(audio_file)
            #         audio_file.seek(0)
            #         playsound(audio_file.name)
            # else:
            #     filename = os.environ['TMP'] + str(time.time()).split('.')[0] + ".mp3"
            #     tts.save(filename)
            #     if _platform == "linux" or _platform == "linux2":
            #         mixer.init()
            #         mixer.music.load(filename)
            #         mixer.music.play()
            #     else:
            #         playsound(filename)
            #     os.remove(filename)
            self.queue_tts.task_done()

    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_tts.put(None)
