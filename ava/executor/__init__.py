from ..queues import QueueCommand, QueuePlugin


class Executor(object):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()
        self.queue_plugin = QueuePlugin()

    def run(self):
        while True:
            command = self.queue_command.get()
            print('Vocal interpretor send : {}'.format(command))
            print('Executor run')
            self.execute_command(command)
            self.queue_command.task_done()

    def execute_command(self, command):
        self.queue_plugin.put(command)
