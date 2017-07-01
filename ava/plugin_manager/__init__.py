from ..queues import QueuePluginManage, QueueTtS
from ..components import _BaseComponent
from ..plugin_store import PluginStore

class PluginManager(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.store = PluginStore()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_tts = QueueTtS()


    def run(self):
        builtin = self.queue_plugin_manage.get()
        print('Plugin manager execute: {}'.format(builtin))
        self.queue_tts.put('builtin handled')
        self.queue_plugin_manage.task_done()
