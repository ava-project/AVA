from .interface import _ListenerInterface
from threading import Thread, Event


class _WindowsInterface(_ListenerInterface):
    """The windows interface responsible of listening each plugin's process
    running.
    """

    def __init__(self, state, store, tts):
        """
        We initialize here the _WindowsInterface by initializing the
        _ListenerInterface with the instances of the State, the PluginStore, the
        queue dedicated to the text-to-speech  component and the queue dedicated
        to the communication between the PluginInvoker and the PluginListener
        (for Windows only, on other operating system listener will be None).

        Args:
            state: The instance of the State object.
            store: The instance of the PluginStore.
            tts: The instance of the queue dedicated to the text-to-speech
                component
        """
        super().__init__(state, store, tts)
        self.plugins = []
        self.threads = []
        self.event = Event()

    def _routine(self, plugin_name, process):
        while not self.event.isSet():
            self._process_result(plugin_name, process)

    def _stop_daemons(self):
        self.event.set()

    def listen(self):
        """Main function of the _WindowsInterface.

        Waits on queue for the name of a plugin running as well as the instance
        of its process. These data are sent to the 'self._process_result' method
        inherited from the _ListenerInterface.
        """
        plugins = []
        for name, _ in self.store.plugins.items():
            plugins.append(name)
        for plugin in list(set(plugins) - set(self.plugins)):
            self.plugins.append(plugin)
            print(self.store.plugins.get(plugin))
            process = self.store.plugins.get(plugin).get_process()
            thread = Thread(target=self._routine, args=(plugin, process))
            self.threads.append(thread)
            thread.daemon = True
            thread.start()
