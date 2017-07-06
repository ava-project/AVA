from ..queues import QueuePluginCommand, QueueTtS
from ..components import _BaseComponent
from ..plugin_store import PluginStore

class PluginRunner(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.store = PluginStore()
        self.queue_plugin_command = QueuePluginCommand()
        self.queue_tts = QueueTtS()

    def run(self):
        """
        """
        command = self.queue_plugin_command.get()
        print('Plugin runner execute : {}'.format(command))
        command = command.split(' ')
        if len(command) < 2:
            self.queue_tts.put('You must specify one command to use the plugin ' + command[0])
            self.queue_plugin_command.task_done()
            return
        if self.store.get_plugin(command[0]):
            if self.store.is_plugin_disabled(command[0]):
                self.queue_tts.put('The plugin ' + command[0] + ' is currently disabled.')
            else:
                process = self.store.get_plugin_process(command[0])
                process.stdin.write(' '.join(command[1:]) + '\n')
                process.stdin.flush()
                result = process.stdout.readline().rstrip()
                self.queue_tts.put(result)
        else:
            self.queue_tts.put('No plugin named ' + command[0] + ' found.')
        self.queue_plugin_command.task_done()
