import os
from ..components import _BaseComponent
from ..plugin_store import PluginStore
from ..queues import QueuePluginManage, QueueTtS
from .plugin_builtins import PluginBuiltins
from ..process import spawn_process
from avasdk.plugins.ioutils.utils import split_string, load_plugin

class PluginManager(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.store = PluginStore()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_tts = QueueTtS()
        self._init()

    def _init(self):
        """
        """
        if not os.path.exists(self.store.path):
            os.makedirs(self.store.path)
            return
        for name in os.listdir(self.store.path):
            plugin = load_plugin(self.store.path, name)
            process = spawn_process(plugin[name])
            self.store.add_plugin(name, plugin[name], process)

    def run(self):
        """
        """
        builtin, plugin = split_string(self.queue_plugin_manage.get(), ' ')
        print('PluginManager:  builtin [{}] plugin [{}]'.format(builtin, plugin))
        if plugin:
            try:
                result = getattr(PluginBuiltins, builtin)(plugin)
                self.queue_tts.put(result)
            except Exception as err:
                self.queue_tts.put('An error occurred with the builtin: ' + builtin + ' for ' + plugin + '.')
        else:
            self.queue_tts.put('Plugin builtin [' + builtin + '] missing 1 argument. Please specify a plugin to ' + builtin + '.')
        self.queue_plugin_manage.task_done()
