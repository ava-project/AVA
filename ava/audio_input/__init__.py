from ..queues import QueueAudio
from ..components import _BaseComponent, RunOneTime


class AudioInput(RunOneTime, _BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue = QueueAudio()

    def setup(self):
        print('seting up Audio')

    def run(self):
        self.queue.put('Input Audio')
