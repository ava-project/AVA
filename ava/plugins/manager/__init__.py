import os
from threading import Timer
from ..plugin import Plugin
from ..store import PluginStore
from .builtins import PluginBuiltins
from ...components import _BaseComponent
from ...queues import QueuePluginManage, QueueTtS
from avasdk.plugins.ioutils.utils import split_string

class PluginManager(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.timer = None
        self.store = PluginStore()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_tts = QueueTtS()
        self._init()
        self._check_plugin_process()

    def _init(self):
        """
        """
        if not os.path.exists(self.store.path):
            os.makedirs(self.store.path)
            return
        for name in os.listdir(self.store.path):
            self.store.add_plugin(name, Plugin(name, self.store.path))

    def _check_plugin_process(self):
        """
        """
        for _, plugin in self.store.plugins.items():
            if not plugin.is_process_alive():
                plugin.restart()
        self.timer = Timer(60, self._check_plugin_process)
        self.timer.start()

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

    def shutdown(self):
        """
        """
        print('Shutting down the PluginManager ...')
        self.timer.cancel()
