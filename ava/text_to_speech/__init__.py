from ..queues import QueueTtS
from ..components import _BaseComponent


class TextToSpeech(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_tts = QueueTtS()

    def run(self):
        sentence = self.queue_tts.get()
        print('To say out loud : {}'.format(sentence))
        self.queue_tts.task_done()
