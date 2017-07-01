from ..queues import QueuePlugin, QueueTtS
from ..components import _BaseComponent
from ..plugin_store import PluginStore

class PluginRunner(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.store = PluginStore()
        self.queue_plugin = QueuePlugin()
        self.queue_tts = QueueTtS()

    def run(self):
        command = self.queue_plugin.get()
        print('Plugin runner execute : {}'.format(command))
        self.queue_tts.put('task completed')
        self.queue_plugin.task_done()
