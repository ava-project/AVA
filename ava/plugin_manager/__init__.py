import os
from ..components import _BaseComponent
from ..plugin_store import PluginStore
from ..queues import QueuePluginManage, QueueTtS
from avasdk.plugins.ioutils.utils import load_plugin
from .plugin_builtins import PluginBuiltins
from ..process import spawn_process

class PluginManager(_BaseComponent):

    def __init__(self):
        '''
        '''
        super().__init__()
        self.store = PluginStore()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_tts = QueueTtS()
        self._init()

    def _init(self):
        '''
        '''
        if not os.path.exists(self.store.path):
            os.makedirs(self.store.path)
            return
        for name in os.listdir(self.store.path):
            plugin = load_plugin(self.store.path, name)
            self.store.add_plugin(name, plugin[name])
            process = spawn_process(name, plugin[name])
            self.store.add_plugin_process(name, process)
            print('process: ', process)
        print(self.store.plugins)

    def run(self):
        '''
        '''
        command = self.queue_plugin_manage.get()
        print('Plugin manager execute : {}'.format(command))
        target = command.split(' ')
        if len(target) > 1:
            try:
                result = getattr(PluginBuiltins, target[0])(str(' '.join(target[1:])))
                self.queue_tts.put(result)
            except Exception as err:
                self.queue_tts.put(str(err))
        else:
            self.queue_tts.put('Plugin builtin [' + target[0] + '] missing 1 argument.')
        self.queue_plugin_manage.task_done()
