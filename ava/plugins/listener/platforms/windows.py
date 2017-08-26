import ctypes
from .interface import _ListenerInterface

class _WindowsInterface(_ListenerInterface):
    """
    """

    def __init__(self, state, store, tts, listener):
        """
        """
        super().__init__(state, store, tts, listener)

    def _popup(self, plugin_name, content):
        """
        """
        ctypes.windll.user32.MessageBoxW(0, content, plugin_name, 1)

    def listen(self):
        """
        """
        plugin_name, process = self.queue_listener.get()
        self._process_result(plugin_name, process)
        self.queue_listener.task_done()
