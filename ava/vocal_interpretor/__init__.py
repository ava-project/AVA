from ..queues import QueueAudio, QueueCommand

class VocalInterpretor(object):

    def __init__(self):
        super().__init__()
        self.queue_audio = QueueAudio()
        self.queue_command = QueueCommand()

    def run(self):
        while True:
            command = input('$> ')
            self.queue_command.put(command)
