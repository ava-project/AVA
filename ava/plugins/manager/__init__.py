import os
from ..plugin import Plugin
from ..store import PluginStore
from .builtins import PluginBuiltins
from ...components import _BaseComponent
from avasdk.plugins.log import Logger


class PluginManager(_BaseComponent):
    """The entity responsible of managing the plugins.

    By this, we mean the management of the installation, uninstallation,
    activation, deactivation of a plugin.
    """

    def __init__(self, queues):
        """Initializer.

        We initilize here the PluginManager by initilizing the _BaseComponent
        class. We also store the instances of the PluginStore.

        Args:
            A dictionary containing all queues instances used acrros the whole
                program.
        """
        super().__init__(queues)
        self.queue_tts = None
        self.queue_manager = None
        self.store = PluginStore()

    def setup(self):
        """This function is executed right after the __init__. We retrieve here
        the instances of the queues used by the PluginManager.
        """
        self.queue_tts = self._queues['QueueTextToSpeech']
        self.queue_manager = self._queues['QueuePluginManager']
        self._init()

    def _init(self):
        """Handler to manager the plugins at the launch of AVA.

        Initialize the folder where the future plugin will be installed.
        Run through this folder and load all the plugins in order to add them
        to the Store and make them available for the whole program.
        """
        if not os.path.exists(self.store.path):
            os.makedirs(self.store.path)
            return
        for name in os.listdir(self.store.path):
            if name in ['__pycache__', '__MACOSX', '.DS_Store']:
                continue
            try:
                self.store.add_plugin(name, Plugin(name, self.store.path))
            except:
                # TODO ensure that the manager tries to install each plugin only once
                # Prevent from having infinite loop spawning many error popups
                import traceback
                print(traceback.format_exc())
                self.queue_tts.put(
                    'Loading of the plugin: {0} failed'.format(name))
                Logger.popup(
                    'Traceback [{0}] Loading of the plugin ({1})'.format(
                        self.__class__.__name__, name), traceback.format_exc())
                continue

    def run(self):
        """The main function of the PluginManager.

        Waits on 'self.queue_manager' for event.
        When an event is enqueued, it invokes the according function of the
        PluginBuiltins depending of the nature of the event.
        """
        while self._is_init:
            try:
                event = self.queue_manager.get()
                if event is None:
                    break
                print('PluginManager: {} {}'.format(event['action'], event['target']))
                if not event['target']:
                    self.queue_tts.put(
                        'In order to use a builtin you must specify one argument.')
                    continue
                self.queue_tts.put(
                    getattr(PluginBuiltins, event['action'])(event['target']))
            except:
                import traceback
                self.queue_tts.put(Logger.unexpected_error(self))
                Logger.popup('Traceback [{0}] {1}: {2}'.format(
                    self.__class__.__name__, event['action'], event['target']),
                             traceback.format_exc())
            finally:
                self.queue_manager.task_done()

    def stop(self):
        """Shutdown gracefully the manager.
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_manager.put(None)
