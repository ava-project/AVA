from tempfile import NamedTemporaryFile

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
        with NamedTemporaryFile() as audio_file:
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            playsound(audio_file.name)
        self.queue_tts.task_done()
