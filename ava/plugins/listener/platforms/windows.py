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
        self._events = {}
        self._watched = {}

    def _routine(self, plugin_name: str, process: subprocess.Popen):
        """
        Thread routine
        """
        while not self._events[plugin_name].isSet():
            self._process_result(plugin_name, process)

    def _stop_daemons(self):
        """
        Stop all threads by setting the internal flag of their 'Event' object to
         True.
        """
        for _, event in self._events.items():
            event.set()

    def listen(self):
        """
        Main function of the _WindowsInterface.

        """
        plugins = list(self._store.get_plugins())
        plugins_restarting = self._state.get_plugins_restarting()
        if len(list(self._watched)) > len(plugins):
            for name in list(set(list(self._watched)) - set(plugins)):
                if name in self._events and not self._events[name].isSet():
                    self._events[name].set()
                if name in self._watched:
                    self._watched.pop(name)
            return
        if len(plugins_restarting) > 0:
            for name in plugins_restarting:
                if name in self._events and not self._events[name].isSet():
                    self._events[name].set()
                if name in self._watched:
                    self._watched.pop(name)
            return
        for name in list(set(plugins) - set(list(self._watched))):
            plugin = self._store.get_plugin(name)
            if plugin is not None and isinstance(plugin, Plugin):
                process = plugin.get_process()
                self._events[name] = threading.Event()
                self._watched[name] = threading.Thread(
                    target=self._routine, args=(name, process))
                self._watched[name].daemon = True
                self._watched[name].start()
