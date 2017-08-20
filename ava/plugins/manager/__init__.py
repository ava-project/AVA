import os
from ..plugin import Plugin
from ..store import PluginStore
from .builtins import PluginBuiltins
from ...components import _BaseComponent
from avasdk.plugins.log import Logger

class PluginManager(_BaseComponent):
    """The entity responsible of managing the plugins. By this, we mean the management
        of the installation, uninstallation, activation, deactivation of a plugin.
        Furthermore, the manager constantly observes the process of each plugin in order
        to ensure that they are functional.
    """

    def __init__(self, queues):
        """Initializer"""
        super().__init__(queues)
        self.queue_tts = None
        self.queue_manager = None
        self.store = PluginStore()

    def setup(self):
        self.queue_tts = self._queues['QueueTextToSpeech']
        self.queue_manager = self._queues['QueuePluginManager']
        self._init()

    def _init(self):
        """Initialize the folder where the future plugin will be installed. Run through this folder
        and load all the plugins in order to add them to the Store and make them available for the
        whole program.
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
                self.queue_tts.put('Loading of the plugin: {0} failed'.format(name))
                continue

    def run(self):
        """The main function of the manager. This function is blocked on the queue.queue
        'self.queue_plugin_manage', waiting for an event.
        """
        while self._is_init:
            try:
                event = self.queue_manager.get()
                if event is None:
                    break
                print('PluginManager: {} {}'.format(event['action'], event['target']))
                if not event['target']:
                    self.queue_tts.put('In order to use a builtin you must specify one argument.')
                    continue
                self.queue_tts.put(getattr(PluginBuiltins, event['action'])(event['target']))
            except:
                import traceback
                traceback.print_exc()
                self.queue_tts.put(Logger.unexpected_error(self))
            finally:
                self.queue_manager.task_done()

    def stop(self):
        """Shutdown gracefully the manager."""
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_manager.put(None)
