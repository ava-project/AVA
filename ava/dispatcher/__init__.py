from ..components import _BaseComponent
from ..state import State
from ..plugins import PluginBuiltins
from avasdk.plugins.builders import build_event


class Dispatcher(_BaseComponent):
    """The Dispatcher class ensures the well forwarding of events."""

    def __init__(self, queues):
        """Initializer."""
        super().__init__(queues)
        self.state = State()
        self.queue_command = None
        self.queue_builtin = None
        self.queue_plugin_manage = None
        self.queue_plugin_command = None
        self.builtin = ['exit', 'open', 'run', 'start', 'launch']

    def setup(self):
        self.queue_command = self._queues['QueueDispatcher']
        self.queue_builtin = self._queues['QueueBuiltinRunner']
        self.queue_plugin_manage = self._queues['QueuePluginManager']
        self.queue_plugin_command = self._queues['QueuePluginInvoker']

    def _waiting_for_specific_event(self, event):
        """Handler to forward an event to the PluginInvoker when this one is expected by AVA.

        param:
            - A dictionary containing the event (dictionary).
        return:
            - A boolean whether a specific event is expected or not.
        """
        waiting, _ = self.state.is_plugin_waiting_for_user_interaction()
        if waiting:
            self.queue_plugin_command.put(event)
            return True
        return False

    def _dispatch_event(self, event):
        """Handler for dispatching the events according their type.

        param:
            - event: A dictionary containing the event to proceed (dictionary).
        """
        if not self._waiting_for_specific_event(event):
            if any(x in event['action'] for x in self.builtin):
                self.queue_builtin.put(event)
            elif any(x in event['action'] for x in PluginBuiltins.builtins):
                self.queue_plugin_manage.put(event)
            else:
                self.queue_plugin_command.put(event)

    def run(self):
        """The main function of the Dispatcher. The Dispatcher is blocked on the
        queue.Queue 'self.queue_command' waiting for an event.
        """
        while self._is_init:
            raw = self.queue_command.get()
            if raw is None:
                break
            event = build_event(raw)
            print('Dispatching...\nVocal interpretor send : {}'.format(raw))
            self._dispatch_event(event)
            self.queue_command.task_done()

    def stop(self):
        """Shutdown gracefully the Dispatcher."""
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_command.put(None)
