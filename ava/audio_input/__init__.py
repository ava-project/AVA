from ..queues import QueueAudio


class AudioInput(object):

    def __init__(self):
        super().__init__()
        self.queue = QueueAudio()

    def run(self):
        self.queue.put('Input Audio')
        print('Done sending a message')
