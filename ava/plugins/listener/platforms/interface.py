import ast
import platform
from ...process import flush_stdout
from ...process import multi_lines_output_handler
from avasdk.plugins.log import Logger

class _ListenerInterface(object):

    def __init__(self, state, store, tts, listener):
        self.state = state
        self.store = store
        self.queue_tts = tts
        self.queue_listener = listener

    def _process_result(self, plugin_name, process):
        """This functions flushes the stdout of the given process and process the
            data read.

        params:
            - plugin_name: The name of the plugin (string).
            - process: The process object (subprocess.Popen)
        """
        output, import_flushed = flush_stdout(process)
        if Logger.ERROR in output:
            self.queue_tts.put('Plugin {} just crashed... Restarting'.format(plugin_name))
            self.store.get_plugin(plugin_name).kill()
            self.store.get_plugin(plugin_name).restart()
            return
        if Logger.IMPORT in output:
            if platform.system() == 'Windows' and self.queue_listener is not None:
                self.queue_listener.put((plugin_name, process))
            return
        if Logger.REQUEST in output:
            output.remove(Logger.REQUEST)
            self.state.plugin_requires_user_interaction(plugin_name)
            self.queue_tts.put(ast.literal_eval(''.join(output)).get('tts'))
            return
        output.remove(Logger.RESPONSE)
        result, multi_lines = multi_lines_output_handler(output)
        if multi_lines:
            self.queue_tts.put('Result of [{}] has been print.'.format(plugin_name))
            Logger.popup(plugin_name, result)
            return
        self.queue_tts.put(result)

    def listen(self):
        """
        """
        raise NotImplementedError()

    def stop(self):
        """
        """
        for _, plugin in self.store.plugins.items():
            plugin.get_process().stdout.close()
