from ..queues import QueueCommand
from ..components import _BaseComponent

class Input(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()

    def run(self):
        command = input('$> ')
        print('Input : {}'.format(command))
        self.queue_command.put(command)
