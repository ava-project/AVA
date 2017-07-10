from ..store import PluginStore
from ...components import _BaseComponent
from ...queues import QueuePluginCommand, QueueTtS
from avasdk.plugins.ioutils.utils import split_string

class PluginInvoker(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.store = PluginStore()
        self.queue_plugin_command = QueuePluginCommand()
        self.queue_tts = QueueTtS()

    def _handle_plugin_execution(self, plugin_name, command):
        """
        """
        # TODO improve this function
        process = self.store.get_plugin(plugin_name).get_process()
        process.stdin.write(command + '\n')
        process.stdin.flush()
        result = process.stdout.readline().rstrip()
        self.queue_tts.put(result)

    def run(self):
        """
        """
        plugin_name, command = split_string(self.queue_plugin_command.get(), ' ')
        print('PluginInvoker searching for: {} ... trying to execute: {}'.format(plugin_name, command))
        if not command:
            self.queue_tts.put('In order to use a plugin, you must specify one command.')
            self.queue_plugin_command.task_done()
            return
        if self.store.is_plugin_disabled(plugin_name):
            self.queue_tts.put('The plugin ' + plugin_name + ' is currently disabled.')
            self.queue_plugin_command.task_done()
            return
        if not self.store.get_plugin(plugin_name):
            self.queue_tts.put('No plugin named ' + plugin_name + ' found.')
        else:
            self._handle_plugin_execution(plugin_name, command)
        self.queue_plugin_command.task_done()

    def shutdown(self):
        """
        """
        print('Shutting down the PluginInvoker ...')
