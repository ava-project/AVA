from ..components import _BaseComponent
from ..plugins import PluginBuiltins


class Dispatcher(_BaseComponent):

    def __init__(self, queues):
        """
        """
        super().__init__(queues)
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
