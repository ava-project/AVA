from ..queues import QueueCommand, QueuePlugin, QueueBuiltin
from ..components import _BaseComponent


class Executor(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_builtin = QueueBuiltin()
        self.queue_command = QueueCommand()
        self.queue_plugin = QueuePlugin()
        self.builtin = ['install', 'uninstall', 'enable', 'disable']

    def run(self):
        command = self.queue_command.get()
        print('Vocal interpretor send : {}'.format(command))
        print('Executor run')
        self.execute_command(command)
        self.queue_command.task_done()

    def execute_command(self, command):
        if any(x in command for x in self.builtin):
            self.queue_builtin.put(command)
        else:
            self.queue_plugin.put(command)
