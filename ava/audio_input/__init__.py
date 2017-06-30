from ..queues import QueueAudio
from ..components import _BaseComponent


class AudioInput(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue = QueueAudio()
        self.loop_on_run = False

    def run(self):
        self.queue.put('Input Audio')
