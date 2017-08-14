import os
import ast
import select
import platform
import threading
from ...state import State
from ..store import PluginStore
from ..process import flush_stdout
from ..process import multi_lines_output_handler
from ...components import _BaseComponent
from ...queues import QueuePluginCommand, QueueTtS
from avasdk.plugins.log import ERROR, IMPORT, REQUEST, RESPONSE

def daemon(fn):
    """@decorator"""
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper

class PluginInvoker(_BaseComponent):
    """The entity responsible of executing the according plugin depending on the user's input."""

    def __init__(self):
        """Initializer."""
        super().__init__()
        self.observer = None
        self.observing = False
        self.stop_observing = threading.Event()
        self.state = State()
        self.store = PluginStore()
        self.queue_plugin_command = QueuePluginCommand()
        self.queue_tts = QueueTtS()

    def _process_result(self, plugin_name, process):
        """This functions flushes the stdout of the given process and process the
            data read.

        params:
            - plugin_name: The name of the plugin (string).
            - process: The process object (subprocess.Popen)
        """
        output, import_flushed = flush_stdout(process)
        if ERROR in output:
            self.queue_tts.put('Plugin {} just crashed... Restarting'.format(plugin_name))
            self.store.get_plugin(plugin_name).kill()
            self.store.get_plugin(plugin_name).restart()
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
            self.queue_tts.put('Result of [{}] has been print.'.format(plugin_name))
        else:
            self.queue_tts.put(result)

    @daemon
    def _observe(self):
        """Thread routine. Polls each plugin process stdout to detect when there is data to read."""
        while not self.stop_observing.is_set():
            if platform.system() == 'Windows':
                FDS = []
                OBSERVED = {}
                for _, plugin in self.store.plugins.items():
                    fd = int(plugin.get_process().stdout.name)
                    OBSERVED[fd] = plugin.get_process()
                    FDS.append(fd)
                try:
                    rlist, wlist, xlist = select.select(FDS, [], [], 0)
                except:
                    raise
                for fd, _ in rlist:
                    if OBSERVED.get(fd) is None:
                        continue
                    p = OBSERVED.get(fd)
                    self._process_result(''.join('{}'.format(k) for k, v in self.store.plugins.items() if p == v.get_process()), p)
            else:
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
        """Execute an event related to a plugin feature.

        params:
            - event: A dictionary containing the event to execute (dictionary).
            - exepected (optional): A boolean to determine if this specific event is expected. (boolean).
            - plugin_name (optional): The name of the plugin waiting for an user input (string).
        """
        if expected:
            self.state.plugin_stops_waiting_for_user_interaction()
            command = ' '.join('{}'.format(value) for key, value in event.items() if value)
        else:
            plugin_name = event['action']
            command = ' '.join('{}'.format(value) for key, value in event.items() if key != 'action' and value)
        assert plugin_name is not None
        process = self.store.get_plugin(plugin_name).get_process()
        assert process is not None
        process.stdin.write(command + '\n')
        process.stdin.flush()

    def _process_event(self, event):
        """Handler to dertimine what kind of event, the invoker is currently dealing with.

        param:
            - event: A dictionary containing the event to proceed (dictionary).
        """
        waiting, plugin = self.state.is_plugin_waiting_for_user_interaction()
        if waiting:
            self._exec_event(event, expected=True, plugin_name=plugin)
            return
        if not event['target']:
            self.queue_tts.put('In order to use a plugin, you must specify one command.')
            return
        if self.store.is_plugin_disabled(event['action']):
            self.queue_tts.put('The plugin {} is currently disabled.'.format(event['action']))
            return
        if not self.store.get_plugin(event['action']):
            self.queue_tts.put('No plugin named {} found.'.format(event['action']))
            return
        self._exec_event(event)

    def run(self):
        """The main function of the invoker.
            Waiting on self.queue_plugin_command, when an event is enqueued, this
            function processes end executes it.
        """
        try:
            if not self.observing:
                self.observing = True
                self._observer = self._observe()
            event = self.queue_plugin_command.get()
            print('PluginInvoker current event: ', event)
            self._process_event(event)
            self.queue_plugin_command.task_done()
        except Exception as err:
            import traceback
            traceback.print_exc()
            self.queue_tts.put(str(err))
            raise

    def shutdown(self):
        """Shutdown gracefully the invoker."""
        print('Shutting down the PluginInvoker ...')
        assert self.observer is not None and not self.stop_observing.is_set()
        self.stop_observing.set()
        self.observer.join()
