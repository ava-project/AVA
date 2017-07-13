from ..queues import QueueTtS
from ..components import _BaseComponent

# import talkey


class TextToSpeech(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_tts = QueueTtS()
        # self.tts = talkey.Talkey(engine_preference=['google', 'espeak'])

    def run(self):
        sentence = self.queue_tts.get()
        print('To say out loud : {}'.format(sentence))
        # self.tts.say(sentence)
        self.queue_tts.task_done()
