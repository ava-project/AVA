

class AudioInput(object):

    def __init__(self, queue_audio):
        super().__init__()
        self.queue = queue_audio

    def run(self):
        self.queue.put('Input Audio')
        print('Done sending a message')
