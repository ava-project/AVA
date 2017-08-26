import time
import platform
import threading
from importlib import import_module
from ...state import State
from ..store import PluginStore
from ...components import _BaseComponent
from avasdk.plugins.log import Logger

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
        queue_listener = None
        klass = '_UnixInterface'
        module = 'ava.plugins.listener.platforms.unix'
        if platform.system() == 'Windows':
            klass = '_WindowsInterface'
            module = 'ava.plugins.listener.platforms.windows'
            queue_listener = self._queues['QueueWindowsListener']
        self.listener = getattr(import_module(module), klass)(State(), PluginStore(),
                                self._queues['QueueTextToSpeech'], queue_listener)

    def run(self):
        """
        """
        while self._is_init:
            try:
                self.listener.listen()
            except:
                import traceback
                traceback.print_exc()
                self._queues['QueueTextToSpeech'].put(Logger.unexpected_error(self))

    def stop(self):
        """
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        if self.listener is not None:
            self.listener.stop()
        PluginStore().clear()
