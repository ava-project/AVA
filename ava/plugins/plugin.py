from os import path
from .process import spawn
from subprocess import Popen
# from ..state import State
# from ..loading import loading
from avasdk.plugins.utils import load_plugin


class Plugin(object):
    """
    A wrapper for a plugin.
    """

    def __init__(self, name: str, path: str):
        """
        We load the plugin's manifest and spawn a process in which the execution
        of the plugin will be contained.

        :name: Plugin name (string).
        :path: Path towards the plugin folder containing the code (string).
        """
        self._name = name
        self._path = path
        self._specs = load_plugin(self._path, self._name)[self._name]
        self._process = spawn(self)

    def __repr__(self):
        return f'<AVA.plugin.name:{self._name.capitalize()}>'

    def get_name(self) -> str:
        """
        :return: A string containing the name of the plugin.
        """
        return self._name

    def get_path(self) -> str:
        """
        :retrurn: Path towards the plugin folder containing the source code.
        """
        return path.join(self._path, self._name)

    def get_process(self) -> Popen:
        """
        :return: The subprocess.Popen instance
        """
        return self._process

    def get_specs(self) -> dict:
        """
        :return: The plugin's manifest.json as dictionary.
        """
        return self._specs

    def kill(self):
        """
        Force kill the plugin's process.

        In case of failure during an attempt to run the plugin, we force kill
        the process and set back 'self._process' to None.
        It ensures to properly restart the plugin after that.
        """
        assert self._process is not None
        self._process.kill()
        self._process = None

    def restart(self):
        """
        Restart the plugin.

        We spawn a new process dedicated to this plugin and we store it into
        'self._process' to make it available and usable again.
        """
        assert self._process is None
        # State().loading()
        # loading(plugins_nbr=1, process_time=6, target=self.name)
        self._process = spawn(self)
        # State().loading_done()

    def shutdown(self):
        """
        Shutdown the plugin gracefully.

        In order to properly shutdown a plugin, we call the 'terminate()'
        method of the subprocess.Popen object and set back 'self.process' to
        None.
        """
        assert self._process is not None
        self._process.terminate()
        self._process = None
