import os
import threading
# local imports
from ..plugin import Plugin
from ..store import PluginStore
from .builtins import PluginBuiltins
from ...components import _BaseComponent
# SDK
from avasdk.plugins.log import Logger


class PluginManager(_BaseComponent):
    """
    The entity responsible of managing the plugins.

    By this, we mean the management of the installation, uninstallation,
    activation, deactivation of a plugin.
    """

    def __init__(self, queues: dict):
        """
        We initilize here the PluginManager by initilizing the _BaseComponent
        class. We also store the instances of the PluginStore.

        :param queues: A dictionary containing all queues instances used acrross
         the whole program.
        """
        super().__init__(queues)
        self._queue_tts = None
        self._queue_manager = None
        self._store = PluginStore()

    def __repr__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>'

    def setup(self):
        """
        This function is executed right after the '__init__'. We retrieve here
        the instances of the queues used by the PluginManager.
        """
        self._queue_tts = self._queues['QueueTextToSpeech']
        self._queue_manager = self._queues['QueuePluginManager']
        self._load_plugins()

    def _load_plugins(self):
        """
        Handler to manage the plugins at the launch of AVA.

        Initialize the folder where the future plugins will be installed.
        Run through this folder and load all the plugins in order to add them
        to the Store and make them available for the whole program.
        """
        targets = []
        if not os.path.exists(self._store.get_path()):
            os.makedirs(self._store.get_path())
            return
        for name in os.listdir(self._store.get_path()):
            if name in ['__pycache__', '__MACOSX', '.DS_Store']:
                continue
            targets.append(name)
        for name in list(set(targets)):
            try:
                self._store.add_plugin(name)
            except:
                import traceback
                print(traceback.format_exc())
                self._queue_tts.put(
                    'Loading of the plugin: {0} failed'.format(name))
                Logger.popup(
                    'Traceback [{0}] Loading of the plugin ({1})'.format(
                        self.__class__.__name__, name), traceback.format_exc())
                continue

    def run(self):
        """
        The main function of the PluginManager.

        Waits on 'self._queue_manager' for event.
        When an event is enqueued, it invokes the according function of the
        PluginBuiltins depending of the nature of the event.
        """
        while self._is_init:
            try:
                event = self._queue_manager.get()
                if event is None:
                    break
                if not event['target']:
                    self._queue_tts.put(
                        'To use a builtin you must specify one argument.')
                    continue
                self._queue_tts.put(
                    getattr(PluginBuiltins, event['action'])(event['target']))
            except:
                import traceback
                self._queue_tts.put(Logger.unexpected_error(self))
                Logger.popup('Traceback [{0}] {1}: {2}'.format(
                    self.__class__.__name__, event['action'], event['target']),
                             traceback.format_exc())
            finally:
                self._queue_manager.task_done()

    def stop(self):
        """
        Shutdown gracefully the manager.
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self._queue_manager.put(None)
