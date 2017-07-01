from ..queues import QueueBuiltin, QueueTtS
from ..components import _BaseComponent

class BuiltinRunner(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_builtin = QueueBuiltin()
        self.queue_tts = QueueTtS()

    def run(self):
        command = self.queue_builtin.get()
        print('Builtin runner execute : {}'.format(command))
        self.queue_tts.put('task completed')
        self.queue_builtin.task_done()
