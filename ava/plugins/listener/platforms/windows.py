from .interface import _ListenerInterface

class _WindowsInterface(_ListenerInterface):
    """
    """

    def __init__(self, state, store, tts, listener):
        """
        """
        super().__init__(state, store, tts, listener)

    def listen(self):
        """
        """
        plugin_name, process = self.queue_listener.get()
        self._process_result(plugin_name, process)
        self.queue_listener.task_done()
