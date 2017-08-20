import platform
from importlib import import_module
from ...state import State
from ..store import PluginStore
from ...components import _BaseComponent
from .platforms import _UnixInterface, _WindowsInterface

class PluginListener(_BaseComponent):
    """
    """

    def __init__(self, queues):
        """
        """
        super().__init__(queues)
        self.listener = None

    def setup(self):
        """
        """
        klass = '_UnixInterface'
        module = 'ava.plugins.listener.platforms.unix'
        if platform.system() == 'Windows':
            klass = '_WindowsInterface'
            module = 'ava.plugins.listener.windows'
        self.listener = getattr(import_module(module), klass)(State(), PluginStore(), self._queues['QueueTextToSpeech'])

    def run(self):
        """
        """
        while self._is_init:
            self.listener.listen()

    def stop(self):
        """
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.listener.stop()
        PluginStore().clear()
