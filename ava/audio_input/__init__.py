from ..queues import QueueAudio
from ..components import _BaseComponent


class AudioInput(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue = QueueAudio()

    def run(self):
        self.queue.put('Input Audio')
