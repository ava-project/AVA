from ..components import _BaseComponent
from ..queues import QueueCommand, QueuePluginCommand, QueuePluginManage, QueueBuiltin


class Dispatcher(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()
        self.queue_builtin = QueueBuiltin()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_plugin_command = QueuePluginCommand()
        # TODO find a better way
        self.builtin = ['help', 'open', 'run', 'start', 'launch']
        self.plugin_manage = ['install', 'uninstall', 'enable', 'disable']

    def run(self):
        command = self.queue_command.get()
        print('Vocal interpretor send : {}'.format(command))
        print('Executor run')
        self.execute_command(command)
        self.queue_command.task_done()

    def execute_command(self, command):
        cmd = command.split(' ')
        # TODO improve the following statements
        if any(x in cmd[0] for x in self.builtin):
            self.queue_builtin.put(command)
        elif any(x in cmd[0] for x in self.plugin_manage):
            self.queue_plugin_manage.put(command)
        else:
            # It will change, and will check if cmd[0] is a known plugin.
            self.queue_plugin_command.put(command)
