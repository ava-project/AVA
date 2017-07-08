from ..queues import QueuePluginCommand, QueueTtS
from ..components import _BaseComponent
from ..plugin_store import PluginStore
from avasdk.plugins.ioutils.utils import split_string

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
        plugin_name, command = split_string(self.queue_plugin_command.get(), ' ')
        print('PluginRunner searching for: {} ... trying to execute: {}'.format(plugin_name, command))
        if not command:
            self.queue_tts.put('In order to use a plugin, you must specify one command.')
            self.queue_plugin_command.task_done()
            return
        if self.store.is_plugin_disabled(plugin_name):
            self.queue_tts.put('The plugin ' + plugin_name + ' is currently disabled.')
            self.queue_plugin_command.task_done()
            return
        if not self.store.get_plugin_process(plugin_name):
            self.queue_tts.put('No plugin named ' + plugin_name + ' found.')
        else:
            # TODO improve this block of code
            process = self.store.get_plugin_process(plugin_name)
            process.stdin.write(command + '\n')
            process.stdin.flush()
            result = process.stdout.readline().rstrip()
            self.queue_tts.put(result)
        self.queue_plugin_command.task_done()
