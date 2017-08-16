from ..queues import QueueCommand
from ..components import _BaseComponent

class NoVocalTest(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()

    def run(self):
        print("Type command and press ENTER ...")
        while self._is_init:
            try:
                cmd = input()
            except EOFError:
                break
            self.queue_command.put(cmd)

    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))