import os
from ...state import State
from ..store import PluginStore
from ..process import flush_process_output
from ..process import clean_outpout_after_runtime_import
from ..process import multi_lines_output_handler
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

    def _process_result_of_plugin_execution(self, plugin_name, command, process):
        """
        """
        ret = flush_process_output(process, ['__END_OF__REQUEST__', '__END_OF_RESPONSE__'])
        output = clean_outpout_after_runtime_import(ret)
        # TODO implement request handling here
        result, multi_lines = multi_lines_output_handler(output)
        if multi_lines:
            print(result)
            self.queue_tts.put('Result of [' + plugin_name + ' ' + command + '] has been print.')
        else:
            self.queue_tts.put(result)

    def _handle_expected_event(self, plugin_name, event):
        """
        """
        self.state.plugin_stops_waiting_for_user_interaction()
        command = (' '.join(value) for key, value in event.items() if value)
        process = self.store.get_plugin(plugin_name).get_process()
        process.stdin.write(command + '\n')
        process.stdin.flush()
        self._process_result_of_plugin_execution(plugin_name, command, process)

    def _handle_common_event(self, event):
        """
        """
        command = ' '.join('{}'.format(value) for key, value in event.items() if key != 'action' and value)
        process = self.store.get_plugin(event['action']).get_process()
        process.stdin.write(command + '\n')
        process.stdin.flush()
        self._process_result_of_plugin_execution(event['action'], command, process)

    def _process_event(self, event):
        """
        """
        if not event['target']:
            self.queue_tts.put('In order to use a plugin, you must specify one command.')
            return
        if self.store.is_plugin_disabled(event['action']):
            self.queue_tts.put('The plugin ' + event['action'] + ' is currently disabled.')
            return
        if not self.store.get_plugin(event['action']):
            self.queue_tts.put('No plugin named ' + event['action'] + ' found.')
        else:
            try:
                self._handle_common_event(event)
            except Exception as err:
                self.queue_tts.put(event['action'] + ' crashed. Restarting ...')

    def _waiting_for_a_specific_event(self, event):
        """
        """
        waiting, plugin_name = self.state.is_plugin_waiting_for_user_interaction()
        if waiting:
            try:
                self._handle_expected_event(plugin_name, event)
            except Exception as err:
                self.queue_tts.put(plugin_name + ' crashed. Restarting ...')
            return True
        return False

    def run(self):
        """
        """
        event = self.queue_plugin_command.get()
        print('PluginInvoker current event: ', event)
        if not self._waiting_for_a_specific_event(event):
            self._process_event(event)
        self.queue_plugin_command.task_done()

    def shutdown(self):
        """
        """
        print('Shutting down the PluginInvoker ...')
