from ..components import _BaseComponent
from ..state import State
from ..plugins import PluginBuiltins
from ..queues import QueueCommand, QueuePluginCommand, QueuePluginManage, QueueBuiltin
from avasdk.plugins.builders import build_event


class Dispatcher(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.state = State()
        self.queue_command = QueueCommand()
        self.queue_builtin = QueueBuiltin()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_plugin_command = QueuePluginCommand()
        self.builtin = ['exit', 'open', 'run', 'start', 'launch']

    def _waiting_for_specific_event(self, event):
        """
        """
        waiting, _ = self.state.is_plugin_waiting_for_user_interaction()
        if waiting:
            self.queue_plugin_command.put(event)
            return True
        return False

    def _dispatch_event(self, event):
        """
        """
        if not self._waiting_for_specific_event(event):
            # TODO update builtins runner
            if any(x in event['action'] for x in self.builtin):
                self.queue_builtin.put(event)
            elif any(x in event['action'] for x in PluginBuiltins.builtins):
                self.queue_plugin_manage.put(event)
            else:
                self.queue_plugin_command.put(event)

    def run(self):
        """
        """
        raw_event = self.queue_command.get()
        event = build_event(raw_event)
        print('Vocal interpretor send : {}'.format(raw_event))
        print('Dispatching ...')
        self._dispatch_event(event)
        self.queue_command.task_done()
