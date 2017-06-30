from ..queues import QueuePlugin, QueueTtS
from ..components import _BaseComponent


class PluginManager(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_plugin = QueuePlugin()
        self.queue_tts = QueueTtS()

    def run(self):
        command = self.queue_plugin.get()
        print('Plugin manager execute : {}'.format(command))
        self.queue_tts.put('task completed')
        self.queue_plugin.task_done()
