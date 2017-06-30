

class TextToSpeech(object):

    def __init__(self, queue_tts):
        super().__init__()
        self.queue_tts = queue_tts

    def run(self):
        while True:
            sentence = self.queue_tts.get()
            print('To say out loud : {}'.format(sentence))
            self.queue_tts.task_done()
