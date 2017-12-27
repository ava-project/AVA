import os
from subprocess import Popen
from avasdk.plugins.log import Logger
from ...state import State
from ..store import PluginStore
from ...components import _BaseComponent


class PluginInvoker(_BaseComponent):
    """
    The PluginInvoker is responsible of runing the according plugin depending
    on the user's input.
    """

    def __init__(self, queues: dict):
        """
        We initilize here the PluginInvoker by initilizing the _BaseComponent
        class. We also store the instances of the PluginStore and the State.

        :param queues: A dictionary containing all queues instances used acrros
         the whole program.
        """
        super().__init__(queues)
        self._state = State()
        self._store = PluginStore()
        self._queue_tts = None
        self._queue_invoker = None

    def __repr__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>'

    def setup(self):
        """
        This function is executed right after the __init__. We retrieve here
        the instances of the queues used by the PluginInvoker.
        """
        self._queue_tts = self._queues['QueueTextToSpeech']
        self._queue_invoker = self._queues['QueuePluginInvoker']

    def _exec_event(self,
                    event: dict,
                    expected: bool=False,
                    plugin_name: str=None):
        """
        This function writes the commmand to run to the stdin file descriptor
        of the process of the plugin concerned.

        :param event: A dictionary containing the command to run (dictionary).
        :param exepected (optional): A boolean to determine if this specific event
         is expected. (boolean).
        :param plugin_name (optional): The name of the plugin waiting for an user
         interaction (string).
        """
        if expected:
            self._state.plugin_stops_waiting_for_user_interaction()
            command = ' '.join('{}'.format(value)
                               for key, value in event.items() if value)
        else:
            plugin_name = event['action']
            command = ' '.join('{}'.format(value)
                               for key, value in event.items()
                               if key != 'action' and value)
        if self._store.get_plugin(plugin_name) is not None:
            process = self._store.get_plugin(plugin_name).get_process()
            if process is not None and isinstance(
                    process, Popen) and not process.stdin.closed:
                process.stdin.write(command + '\n')
                process.stdin.flush()

    def _process_event(self, event: dict):
        """
        Processes the given event.

        The event is processed to determine firstly if this one is expected.
        In case of a plugin has been executed, and the completion of this
        execution requires an interaction of the user, the event is
        automatically forward to the plugin waiting.
        Otherwise, the event is parsed to ensure that it contains all the
        required information to run a plugin.

        :param event: A dictionnary representing the event.
        """
        waiting, plugin = self._state.is_plugin_waiting_for_user_interaction()
        if waiting:
            self._exec_event(event, expected=True, plugin_name=plugin)
            return
        elif not event['target']:
            self._queue_tts.put(
                'In order to use a plugin, you must specify one command.')
            return
        elif self._store.is_plugin_disabled(event['action']):
            self._queue_tts.put(
                'The plugin {} is currently disabled.'.format(event['action']))
            return
        elif not self._store.get_plugin(event['action']):
            self._queue_tts.put(
                'No plugin named {} found.'.format(event['action']))
            return
        else:
            self._exec_event(event)

    def run(self):
        """
        This is the main function of the PluginInvoker.

        Designed in an infinite loop, the PluginInvoker is waiting on a queue
        for an event to process.
        """
        while self._is_init:
            try:
                event = self._queue_invoker.get()
                if event is None:
                    break
                self._process_event(event)
            except:
                import traceback
                self._queue_tts.put(Logger.unexpected_error(self))
                Logger.popup('Traceback [{0}] invoking: {1} {2}'.format(
                    self.__class__.__name__, event['action'], event['target']),
                             traceback.format_exc())
            finally:
                self._queue_invoker.task_done()

    def stop(self):
        """
        Shutdown gracefully the PluginInvoker

        In order to shutdown the PluginInvoker which is running in an infinite
        loop, we set the value of 'self._is_init' to False and we enqueue 'None'
        in 'self.queue_invoker' to break the loop.
        We also go through all the plugins stored in the store and close the
        stdin file descriptor of each process.
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self._queue_invoker.put(None)
        for _, plugin in self._store.get_plugins().items():
            process = plugin.get_process()
            if process is not None and isinstance(process, Popen):
                process.stdin.close()
