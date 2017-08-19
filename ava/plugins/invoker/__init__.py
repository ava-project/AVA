import os
from ...state import State
from ..store import PluginStore
from ...components import _BaseComponent


class PluginInvoker(_BaseComponent):
    """The entity responsible of executing the according plugin depending on the user's input."""

    def __init__(self, queues):
        """Initializer."""
        super().__init__(queues)
        self.state = State()
        self.store = PluginStore()
        self.queue_plugin_command = None
        self.queue_tts = None

    def setup(self):
        self.queue_plugin_command = self._queues['QueuePluginInvoker']
        self.queue_tts = self._queues['QueueTextToSpeech']

    def _exec_event(self, event, expected=False, plugin_name=None):
        """Execute an event related to a plugin feature.

        params:
            - event: A dictionary containing the event to execute (dictionary).
            - exepected (optional): A boolean to determine if this specific event is expected. (boolean).
            - plugin_name (optional): The name of the plugin waiting for an user input (string).
        """
        if expected:
            self.state.plugin_stops_waiting_for_user_interaction()
            command = ' '.join('{}'.format(value) for key, value in event.items() if value)
        else:
            plugin_name = event['action']
            command = ' '.join('{}'.format(value) for key, value in event.items() if key != 'action' and value)
        assert plugin_name is not None
        process = self.store.get_plugin(plugin_name).get_process()
        assert process is not None and not process.stdin.closed
        process.stdin.write(command + '\n')
        process.stdin.flush()

    def _process_event(self, event):
        """Handler to dertimine what kind of event, the invoker is currently dealing with.

        param:
            - event: A dictionary containing the event to proceed (dictionary).
        """
        waiting, plugin = self.state.is_plugin_waiting_for_user_interaction()
        if waiting:
            self._exec_event(event, expected=True, plugin_name=plugin)
            return
        if not event['target']:
            self.queue_tts.put('In order to use a plugin, you must specify one command.')
            return
        if self.store.is_plugin_disabled(event['action']):
            self.queue_tts.put('The plugin {} is currently disabled.'.format(event['action']))
            return
        if not self.store.get_plugin(event['action']):
            self.queue_tts.put('No plugin named {} found.'.format(event['action']))
            return
        self._exec_event(event)

    def run(self):
        """The main function of the PluginInvoker.
            This function is blocked, waiting on the queue.Queue 'self.queue_plugin_command'
            for an event.
        """
        while self._is_init:
            try:
                event = self.queue_plugin_command.get()
                if event is None:
                    break
                print('PluginInvoker current event: ', event)
                self._process_event(event)
                self.queue_plugin_command.task_done()
            except:
                import traceback
                traceback.print_exc()
                raise

    def stop(self):
        """Shutdown gracefully the PluginInvoker."""
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_plugin_command.put(None)
