from ..components import _BaseComponent
from ..state import State
from ..plugins import PluginBuiltins
from ..queues import QueueCommand, QueuePluginCommand, QueuePluginManage, QueueBuiltin
from avasdk.plugins.builders import build_event


class Dispatcher(_BaseComponent):
    """The Dispatcher class ensures the well forwarding of events."""

    def __init__(self):
        """Initializer."""
        super().__init__()
        self.state = State()
        self.queue_command = QueueCommand()
        self.queue_builtin = QueueBuiltin()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_plugin_command = QueuePluginCommand()
        self.builtin = ['exit', 'open', 'run', 'start', 'launch']

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
        raw = self.queue_command.get()
        event = build_event(raw)
        print('Dispatching...\nVocal interpretor send : {}'.format(raw))
        self._dispatch_event(event)
        self.queue_command.task_done()

    def shutdown(self):
        """Shutdown gracefully the Dispatcher."""
        print('Shutting down the Dispatcher')
