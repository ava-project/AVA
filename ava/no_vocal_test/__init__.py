from ..components import _BaseComponent
from ..config import ConfigLoader

class NoVocalTest(_BaseComponent):

    def __init__(self, queues):
        super().__init__(queues)
        self.queue_command = None
        self.config = ConfigLoader(None, None)

    def setup(self):
        self.queue_command = self._queues['QueueDispatcher']

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