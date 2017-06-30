

class Executor(object):

    def __init__(self, queue_command, queue_plugin):
        super().__init__()
        self.queue_command = queue_command
        self.queue_plugin = queue_plugin

    def run(self):
        while True:
            command = self.queue_command.get()
            print('Vocal interpretor send : {}'.format(command))
            print('Executor run')
            self.execute_command(command)
            self.queue_command.task_done()

    def execute_command(self, command):
        self.queue_plugin.put(command)
