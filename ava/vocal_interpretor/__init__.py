

class VocalInterpretor(object):

    def __init__(self, queue_audio, queue_command):
        super().__init__()
        self.queue_audio = queue_audio
        self.queue_command = queue_command

    def run(self):
        while True:
            command = input('$> ')
            self.queue_command.put(command)
