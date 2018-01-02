import ast
import queue
import platform
import subprocess
# local imports
from ...plugin import Plugin
from ...store import PluginStore
from ...utils import State, flush_stdout, multi_lines_output_handler
# SDK
from avasdk.plugins.log import Logger


class _ListenerInterface(object):
    """
    """

    def __init__(self, state: State, store: PluginStore, tts: queue.Queue):
        """
        """
        self._state = state
        self._store = store
        self._queue_tts = tts

    def __repr__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>'

    def _process_result(self, plugin_name: str, process: subprocess.Popen):
        """
        This function is called when an event has been detected on the stdout
        file descriptor of a plugin's process.
        It flushes the data print on the stdout of the process and processes it.
        A message is enqueued in 'self._queue_tts' which is the queue dedicated
        to the text-to-speech component. It allows us to perform a feedback to
        the user about the command which he/she has just dictated.

        :param plugin_name: The name of the plugin (string).
        :param process: The instance of the subprocess.Popen object of a plugin
         (subprocess.Popen).
        """
        output, import_flushed = flush_stdout(process)
        if Logger.ERROR in output:
            output.remove(Logger.ERROR)
            self._queue_tts.put(
                'Plugin {} just crashed... Restarting'.format(plugin_name))
            Logger.popup(
                'Traceback - Plugin [{0}] previous command FAILED'.format(
                    plugin_name), output)
            plugin = self._store.get_plugin(plugin_name)
            if plugin is not None and isinstance(plugin, Plugin):
                plugin.kill()
                plugin.restart()
            return
        elif Logger.IMPORT in output:
            return
        elif Logger.REQUEST in output:
            output.remove(Logger.REQUEST)
            self._state.plugin_requires_user_interaction(plugin_name)
            self._queue_tts.put(ast.literal_eval(''.join(output)).get('tts'))
            return
        else:
            output.remove(Logger.RESPONSE)
            result, multi_lines = multi_lines_output_handler(output)
            if multi_lines:
                self._queue_tts.put(
                    'Result of [{}] has been print.'.format(plugin_name))
                Logger.popup(plugin_name, result)
                return
            self._queue_tts.put(result)

    def listen(self):
        """
        The main function of the listener.

        It must be implemented by the interface. Raises an error if this method
        is not implemented in the interface inheriting from _ListenerInterface.
        """
        raise NotImplementedError()

    def stop(self):
        """
        Stop the listener.

        We go through all plugins and close the stdout file descriptor of each
        process for each plugin.
        """
        if platform.system() == 'Windows':
            self._stop_daemons()
        for _, plugin in self._store.get_plugins().items():
            process = plugin.get_process()
            if process is not None and isinstance(
                    process, subprocess.Popen) and not process.stdout.closed:
                process.stdout.close()
