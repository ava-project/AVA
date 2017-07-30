import os
from threading import Timer
from ..plugin import Plugin
from ..store import PluginStore
from .builtins import PluginBuiltins
from ...components import _BaseComponent
from ...queues import QueuePluginManage, QueueTtS

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
            if name in ['__pycache__', '__MACOSX', '.DS_Store']:
                continue
            try:
                self.store.add_plugin(name, Plugin(name, self.store.path))
            except Exception as err:
                print(str(err))
                continue

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
        event = self.queue_plugin_manage.get()
        print('PluginManager:  builtin [{}] plugin [{}]'.format(event['action'], event['target']))
        if event['target']:
            try:
                result = getattr(PluginBuiltins, event['action'])(event['target'])
                self.queue_tts.put(result)
            except Exception as err:
                print(str(err))
                self.queue_tts.put('An error occurred with the builtin: ' + event['action'] + ' for ' + event['target'] + '.')
        else:
            self.queue_tts.put('Plugin builtin [' + event['action'] + '] missing 1 argument. Please specify a plugin to ' + event['action'] + '.')
        self.queue_plugin_manage.task_done()

    def shutdown(self):
        """
        """
        print('Shutting down the PluginManager ...')
        self.timer.cancel()
        self.store.clear()
