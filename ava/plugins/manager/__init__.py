import os
from threading import Timer
from ..plugin import Plugin
from ..store import PluginStore
from .builtins import PluginBuiltins
from ...components import _BaseComponent
from avasdk.plugins.ioutils.utils import split_string

class PluginManager(_BaseComponent):

    def __init__(self, queues):
        """
        """
        super().__init__(queues)
        self.timer = None
        self.store = PluginStore()
        self.queue_plugin_manage = None
        self.queue_tts = None
        self._init()
        self._check_plugin_process()

    def setup(self):
        self.queue_plugin_manage = self._queues['QueuePluginManager']
        self.queue_tts = self._queues['QueueTextToSpeech']

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
        self.timer = Timer(10, self._check_plugin_process)
        self.timer.start()

    def run(self):
        """
        """
        while self._is_init:
            cmd = self.queue_plugin_manage.get()
            if cmd is None:
                break
            builtin, plugin = split_string(cmd, ' ')
            print('PluginManager:  builtin [{}] plugin [{}]'.format(builtin, plugin))
            if plugin:
                try:
                    result = getattr(PluginBuiltins, builtin)(plugin)
                    self.queue_tts.put(result)
                except Exception as err:
                    self.queue_tts.put(str(err))
                    # self.queue_tts.put('An error occurred with the builtin: ' + builtin + ' for ' + plugin + '.')
            else:
                self.queue_tts.put('Plugin builtin [' + builtin + '] missing 1 argument. Please specify a plugin to ' + builtin + '.')
            self.queue_plugin_manage.task_done()

    def shutdown(self):
        """
        """
        print('Shutting down the PluginManager ...')
        self.timer.cancel()
        self.store.clear()

    def stop(self):
        print('Stopping the PluginManager')
        self._is_init = False
        self.queue_plugin_manage.put(None)
        self.shutdown()