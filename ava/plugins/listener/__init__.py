import time
import platform
import threading
from importlib import import_module
from ...state import State
from ..store import PluginStore
from ...components import _BaseComponent
from avasdk.plugins.log import Logger


class PluginListener(_BaseComponent):
    """The entity responsible to watch the process of each plugin installed and
    running in order to detect when the result of their execution requires to be
    processed.
    """

    def __init__(self, queues):
        """Initializer.

        We initialize the PluginListener here by initializing the _BaseComponent
        class.

        Args:
            A dictionary containing all queues instances used acrros the whole
                program.
        """
        super().__init__(queues)
        self.listener = None

    def setup(self):
        """This function is called right after the '__init__'.

        We determine here which interface we are going to use to watch the
        plugins depending of the user's operating system.
        """
        queue_listener = None
        klass = '_UnixInterface'
        module = 'ava.plugins.listener.platforms.unix'
        if platform.system() == 'Windows':
            klass = '_WindowsInterface'
            module = 'ava.plugins.listener.platforms.windows'
            queue_listener = self._queues['QueueWindowsListener']
        self.listener = getattr(import_module(module), klass)(
            State(),
            PluginStore(),
            self._queues['QueueTextToSpeech'],
            queue_listener
        )

    def run(self):
        """The main function of the PluginListener.

        Designed as an infinite loop, The PluginListener is constantly listening
        the plugins installed in order to process the result of their execution
        and perform a feedback to the user.
        """
        while self._is_init:
            try:
                self.listener.listen()
            except:
                import traceback
                self._queues['QueueTextToSpeech'].put(
                    Logger.unexpected_error(self))
                Logger.popup('Traceback [{0}]'.format(self.__class__.__name__),
                             traceback.format_exc())

    def stop(self):
        """Shutdown gracefull the PluginListener.

        In order to break the infinite loop, we set 'self._is_init' to False.
        We call the 'stop()' method the listener.
        We clear the PluginStore here because the PluginListener is the last
        component called in case of shutdown.
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        if self.listener is not None:
            self.listener.stop()
        PluginStore().clear()
