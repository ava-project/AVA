from .interface import _ListenerInterface


class _WindowsInterface(_ListenerInterface):
    """The windows interface responsible of listening each plugin's process
    running.
    """

    def __init__(self, state, store, tts, listener):
        """Initializer.

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
            listener: The  instance of the queue dedicated to the communication
                between the PluginInvoker and the PluginListener (on Windows
                only, otherwise 'None')
        """
        super().__init__(state, store, tts, listener)

    def listen(self):
        """Main function of the _WindowsInterface.

        Waits on queue for the name of a plugin running as well as the instance
        of its process. These data are sent to the 'self._process_result' method
        inherited from the _ListenerInterface.
        """
        plugin_name, process = self.queue_listener.get()
        self._process_result(plugin_name, process)
        self.queue_listener.task_done()
