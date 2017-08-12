import os
import ast
import select
import threading
from ...state import State
from ..store import PluginStore
from ..process import flush_process_output
from ..process import multi_lines_output_handler
from ...components import _BaseComponent
from ...queues import QueuePluginCommand, QueueTtS
from avasdk.plugins.log import ERROR, IMPORT, REQUEST, RESPONSE

def daemon(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper

class PluginInvoker(_BaseComponent):

    def __init__(self):
        """
        """
        super().__init__()
        self.observer = None
        self.observing = False
        self.stop_observing = threading.Event()
        self.state = State()
        self.store = PluginStore()
        self.queue_plugin_command = QueuePluginCommand()
        self.queue_tts = QueueTtS()

    def _process_result(self, plugin_name, process):
        """
        """
        output, import_flushed = flush_process_output(process)
        if ERROR in output:
            self.queue_tts.put('Plugin ' + plugin_name + 'j ust crashed... Restarting')
            return
        if IMPORT in output:
            return
        if REQUEST in output:
            output.remove(REQUEST)
            self.state.plugin_requires_user_interaction(plugin_name)
            self.queue_tts.put(ast.literal_eval(''.join(output)).get('tts'))
            return
        output.remove(RESPONSE)
        # TODO improve this part
        result, multi_lines = multi_lines_output_handler(output)
        if multi_lines:
            print(result)
            self.queue_tts.put('Result of [' + plugin_name + '] has been print.')
        else:
            self.queue_tts.put(result)

    @daemon
    def _observe(self):
        """
        """
        while not self.stop_observing.is_set():
            OBSERVED = {}
            POLL = select.poll()
            READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
            for _, plugin in self.store.plugins.items():
                fd = int(plugin.get_process().stdout.name)
                OBSERVED[fd] = plugin.get_process()
                POLL.register(fd, READ_ONLY)
            try:
                result = POLL.poll(0)
            except:
                raise
            for fd, _ in result:
                if OBSERVED.get(fd) is None:
                    continue
                p = OBSERVED.get(fd)
                self._process_result(''.join('{}'.format(k) for k, v in self.store.plugins.items() if p == v.get_process()), p)

    def _exec_event(self, event, expected=False, plugin_name=None):
        """
        """
        if expected:
            self.state.plugin_stops_waiting_for_user_interaction()
            command = ' '.join('{}'.format(value) for key, value in event.items() if value)
        else:
            plugin_name = event['action']
            command = ' '.join('{}'.format(value) for key, value in event.items() if key != 'action' and value)
        assert plugin_name is not None
        process = self.store.get_plugin(plugin_name).get_process()
        process.stdin.write(command + '\n')
        process.stdin.flush()

    def _process_event(self, event):
        """
        """
        waiting, plugin = self.state.is_plugin_waiting_for_user_interaction()
        if waiting:
            self._exec_event(event, expected=True, plugin_name=plugin)
            return
        if not event['target']:
            self.queue_tts.put('In order to use a plugin, you must specify one command.')
            return
        if self.store.is_plugin_disabled(event['action']):
            self.queue_tts.put('The plugin ' + event['action'] + ' is currently disabled.')
            return
        if not self.store.get_plugin(event['action']):
            self.queue_tts.put('No plugin named ' + event['action'] + ' found.')
            return
        self._exec_event(event)

    def run(self):
        """
        """
        try:
            if not self.observing:
                self.observing = True
                self._observer = self._observe()
            event = self.queue_plugin_command.get()
            print('PluginInvoker current event: ', event)
            self._process_event(event)
            self.queue_plugin_command.task_done()
        except:
            import traceback
            traceback.print_exc()
            self.queue_tts.put('RuntimeError')
            raise

    def shutdown(self):
        """
        """
        print('Shutting down the PluginInvoker ...')
        assert self.observer is not None
        self.stop_observing.set()
