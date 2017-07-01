from ..queues import QueueBuiltin, QueueTtS
from ..components import _BaseComponent
from ..plugin_store import PluginStore

class PluginManager(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.store = PluginStore()
        self.queue_builtin = QueueBuiltin()
        self.queue_tts = QueueTtS()


    def run(self):
        builtin = self.queue_builtin.get()
        print('Plugin manager execute: {}'.format(builtin))
        self.queue_tts.put('builtin handled')
        self.queue_builtin.task_done()
