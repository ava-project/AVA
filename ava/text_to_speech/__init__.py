from ..queues import QueueTtS
from ..components import _BaseComponent
from gtts import gTTS
from pygame import mixer

import os


class TextToSpeech(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_tts = QueueTtS()

    def run(self):
        sentence = self.queue_tts.get()
        print('To say out loud : {}'.format(sentence))
        # TODO change the language to match user's settings
        tts = gTTS(text=sentence, lang='en')
        tts.save("tts.mp3")
        mixer.init()
        mixer.music.load("tts.mp3")
        mixer.music.play()
        os.remove("tts.mp3")
        self.queue_tts.task_done()
