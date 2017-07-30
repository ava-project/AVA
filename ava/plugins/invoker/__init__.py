import os
from ..store import PluginStore
from ..process import flush_process_output
from ...state import State
from ...components import _BaseComponent
from ...queues import QueuePluginCommand, QueueTtS
from avasdk.plugins.ioutils.utils import split_string

class PluginInvoker(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.state = State()
        self.store = PluginStore()
        self.queue_plugin_command = QueuePluginCommand()
        self.queue_tts = QueueTtS()

    def _handle_plugin_execution(self, plugin_name, command):
        """
        """
        try:
            plugin, state = self.state.get_plugin_state()
            if state:
                print('Command: {} for plugin: {}'.format(command, plugin))
                self.state.set_plugin_state()
            process = self.store.get_plugin(plugin_name).get_process()
            process.stdin.write(command + '\n')
            process.stdin.flush()
            ret = flush_process_output(process, 'END_OF_COMMAND')
            if 'END_OF_IMPORT' in ret:
                index = 0
                target = ret.index('END_OF_IMPORT')
                while index <= target:
                    ret.remove(index)
                    index += 1
            if len(ret) > 1:
                print('\n'.join(ret))
                self.queue_tts.put('Result of [' + plugin_name + ' ' + command + '] has been print.')
                return
            self.queue_tts.put(''.join(ret))
        except Exception as err:
            self.queue_tts.put(plugin_name + ' crashed. Restarting ...')

    def run(self):
        """
        """
        event = self.queue_plugin_command.get()
        plugin, state = self.state.get_plugin_state()
        if state:
            self._handle_plugin_execution(plugin, event)
            self.queue_plugin_command.task_done()
            return
        plugin_name, command = split_string(event, ' ')
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
