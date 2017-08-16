from ..components import _BaseComponent
from ..plugins import PluginBuiltins
from ..queues import QueueCommand, QueuePluginCommand, QueuePluginManage, QueueBuiltin


class Dispatcher(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.queue_command = QueueCommand()
        self.queue_builtin = QueueBuiltin()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_plugin_command = QueuePluginCommand()
        self.builtin = ['exit', 'open', 'run', 'start', 'launch']

    def _execute_command(self, command):
        """
        """
        cmd = command.split(' ')
        # TODO improve the following statements
        if any(x in cmd[0] for x in self.builtin):
            self.queue_builtin.put(command)
        elif any(x in cmd[0] for x in PluginBuiltins.builtins):
            self.queue_plugin_manage.put(command)
        else:
            self.queue_plugin_command.put(command)

    def run(self):
        """
        """
        while self._is_init:
            command = self.queue_command.get()
            if command is None:
                break
            print('Vocal interpretor send : {}'.format(command))
            print('Dispatching ...')
            self._execute_command(command)
            self.queue_command.task_done()

    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_command.put(None)
