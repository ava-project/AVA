from ..queues import QueueCommand
from ..components import _BaseComponent



class NoVocalTest(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()

    def run(self):
        print("Type command and press ENTER ...")
        cmd = input()
        self.queue_command.put(cmd)