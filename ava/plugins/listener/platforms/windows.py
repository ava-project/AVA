import queue
import threading
import subprocess
# local imports
from ...utils import State
from ...plugin import Plugin
from ...store import PluginStore
from .interface import _ListenerInterface


class _WindowsInterface(_ListenerInterface):
    """
    The Windows interface responsible of detecting an I/O event on the standard
    output stream of a plugin process.
    """

    def __init__(self, state: State, store: PluginStore, tts: queue.Queue):
        """
        We initialize here the _WindowsInterface by initializing the
        _ListenerInterface with the instances of the State, the PluginStore, the
        queue dedicated to the text-to-speech  component.

        :param state: The instance of the State object.
        :param store: The instance of the PluginStore.
        :param tts: The instance of the queue dedicated to the text-to-speech
         component
        """
        super().__init__(state, store, tts)
        self._plugins = []
        self._threads = []
        self._event = threading.Event()

    def _routine(self, plugin_name: str, process: subprocess.Popen):
        """
        Thread routine
        """
        while not self._event.isSet():
            self._process_result(plugin_name, process)

    def _stop_daemons(self):
        """
        Stop all threads by setting the internal flag of the 'Event' object to
         True.
        """
        self._event.set()

    def listen(self):
        """
        Main function of the _WindowsInterface.

        Waits on queue for the name of a plugin running as well as the instance
        of its process. These data are sent to the 'self._process_result' method
        inherited from the _ListenerInterface.
        """
        plugins = [x for x in self._store.get_plugins().keys()]
        for plugin in list(set(plugins) - set(self._plugins)):
            self._plugins.append(plugin)
            process = self._store.get_plugin(plugin).get_process()
            thread = threading.Thread(
                target=self._routine, args=(plugin, process))
            self._threads.append(thread)
            thread.daemon = True
            thread.start()
