import ast
import select
from ...process import flush_stdout
from .interface import _ListenerInterface
from ...process import multi_lines_output_handler
from avasdk.plugins.log import ERROR, IMPORT, REQUEST, RESPONSE

class _UnixInterface(_ListenerInterface):
    """
    """

    def __init__(self, state, store, tts):
        """
        """
        super().__init__(state, store, tts)

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
        result, multi_lines = multi_lines_output_handler(output)
        if multi_lines:
            # TODO Spawn a window and print the multi lines output
            print(result)
            self.queue_tts.put('Result of [{}] has been print.'.format(plugin_name))
        else:
            self.queue_tts.put(result)

    def listen(self):
        """
        """
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

    def stop(self):
        """
        """
        for _, plugin in self.store.plugins.items():
            plugin.get_process().stdout.close()
