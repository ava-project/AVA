import ast
from time import sleep
from ...process import flush_stdout
from .interface import _ListenerInterface
from ...process import multi_lines_output_handler
from avasdk.plugins.log import Logger

class _WindowsInterface(_ListenerInterface):
    """
    """

    def __init__(self, state, store, tts):
        """
        """
        super().__init__(state, store, tts)
        self.queue = None

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
            self.queue.put(plugin_name)
            return
        if Logger.REQUEST in output:
            output.remove(Logger.REQUEST)
            self.state.plugin_requires_user_interaction(plugin_name)
            self.queue_tts.put(ast.literal_eval(''.join(output)).get('tts'))
            return
        output.remove(Logger.RESPONSE)
        result, multi_lines = multi_lines_output_handler(output)
        if multi_lines:
            # TODO Spawn a window and print the multi lines output
            print(result)
            self.queue_tts.put('Result of [{}] has been print.'.format(plugin_name))
        else:
            self.queue_tts.put(result)

    def listen(self, *args, **kwargs):
        """
        """
        # TODO find a way to handle it on Windows
        self.queue = args[0]
        plugin_name = self.queue.get()
        process = self.store.get_plugin(plugin_name).get_process()
        self._process_result(plugin_name, process)
        self.queue.task_done()

    def stop(self):
        """
        """
        print('Stop _WindowsInterface')
