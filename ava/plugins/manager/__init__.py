import os
from threading import Timer
from ..plugin import Plugin
from ..store import PluginStore
from .builtins import PluginBuiltins
from ...components import _BaseComponent
from ...queues import QueuePluginManage, QueueTtS

class PluginManager(_BaseComponent):
    """The entity responsible of managing the plugins. By this, we mean the management
        of the installation, uninstallation, activation, deactivation of a plugin.
        Furthermore, the manager constantly observes the process of each plugin in order
        to ensure that they are functional
    """

    def __init__(self):
        """Initializer
        """
        super().__init__()
        self.timer = None
        self.store = PluginStore()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_tts = QueueTtS()
        self._init()
        self._observe()

    def _init(self):
        """Loads the plugins.
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

    def _observe(self):
        """Handler to constantly watch each plugin process and ensure that they
            are always functional.
        """
        for _, plugin in self.store.plugins.items():
            if plugin.get_process() is None:
                plugin.restart()
        self.timer = Timer(60, self._observe)
        self.timer.start()

    def run(self):
        """The main function of the manager. This function is blocked on self.queue_plugin_manage
            until an event is enqueued.
        """
        try:
            event = self.queue_plugin_manage.get()
            plugin = event['target']
            builtin = event['action']
            print('PluginManager: {} {}'.format(builtin, plugin))
            if plugin:
                try:
                    self.queue_tts.put(getattr(PluginBuiltins, builtin)(plugin))
                except Exception as err:
                    self.queue_tts.put('An error occurred with the builtin: {} for {}.'.format(builtin, plugin))
                    raise
            else:
                self.queue_tts.put('Plugin builtin [{}] missing 1 argument. Please specify a plugin to {}.'.format(builtin, builtin))
            self.queue_plugin_manage.task_done()
        except:
            import traceback
            traceback.print_exc()
            raise

    def shutdown(self):
        """Shutdown gracefully the manager.
        """
        print('Shutting down the PluginManager ...')
        self.timer.cancel()
        self.store.clear()
