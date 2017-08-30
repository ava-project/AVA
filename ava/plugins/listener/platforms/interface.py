import ast
import platform
from ...process import flush_stdout
from ...process import multi_lines_output_handler
from avasdk.plugins.log import Logger


class _ListenerInterface(object):
    """
    """

    def __init__(self, state, store, tts, listener):
        """
        """
        self.state = state
        self.store = store
        self.queue_tts = tts
        self.queue_listener = listener

    def _process_result(self, plugin_name, process):
        """This function is called when an event has been detected on the stdout
        file descriptor of a plugin's process.
        It flushes the data print on the stdout of the process and processes it.
        A message is enqueued in 'self.queue_tts' which is the queue dedicated
        to the text-to-speech component. It allows us to perform a feedback to
        the user about the command which he/she has just dictated.

        Args:
            plugin_name: The name of the plugin (string).
            process: The instance of the subprocess.Popen object of a plugin
                (subprocess.Popen).
        """
        output, import_flushed = flush_stdout(process)
        if Logger.ERROR in output:
            output.remove(Logger.ERROR)
            self.queue_tts.put(
                'Plugin {} just crashed... Restarting'.format(plugin_name))
            Logger.popup(
                'Traceback - Plugin [{0}] previous command FAILED'.format(
                    plugin_name), output)
            self.store.get_plugin(plugin_name).kill()
            self.store.get_plugin(plugin_name).restart()
            return
        if Logger.IMPORT in output:
            if platform.system() == 'Windows' and self.queue_listener:
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
            self.queue_tts.put(
                'Result of [{}] has been print.'.format(plugin_name))
            Logger.popup(plugin_name, result)
            return
        self.queue_tts.put(result)

    def listen(self):
        """The main function of the listener.

        It must be implemented by the interface. Raises an error if this method
        is not implemented in the interface inheriting from _ListenerInterface.
        """
        raise NotImplementedError()

    def stop(self):
        """Stop the listener.

        We go through all plugins and close the stdout file descriptor of each
        process for each plugin.
        """
        for _, plugin in self.store.plugins.items():
            plugin.get_process().stdout.close()
