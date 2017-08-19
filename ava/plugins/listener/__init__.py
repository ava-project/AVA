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

    def setup(self):
        """
        """
        flag = platform.system == 'Windows'
        path = 'ava.plugins.listener.platforms.'
        interface = '_WindowsInterface' if flag else '_UnixInterface'
        module = import_module(path + 'windows') if flag else import_module(path + 'unix')
        self.listener = getattr(module, interface)(State(), PluginStore(), self._queues['QueueTextToSpeech'])

    def run(self):
        """
        """
        while self._is_init:
            self.listener.run()

    def stop(self):
        """
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.listener.stop()
