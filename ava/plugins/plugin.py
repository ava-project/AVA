from os.path import join
from subprocess import Popen
from avasdk.plugins.utils import load_plugin
from .process import spawn
from ..state import State

__all__ = ['State']


class Plugin(object):
    """
    A wrapper for a plugin.
    """

    def __init__(self, name: str, path: str):
        """
        We load the plugin's manifest and spawn a process in which the execution
        of the plugin will be contained.

        :param name: Plugin name.
        :param path: Path towards the plugin folder containing the code.
        """
        self._name = name
        self._path = path
        self._specs = load_plugin(self._path, self._name)[self._name]
        self._process = spawn(self)

    def __repr__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__name__} {self._name.capitalize()} at {hex(id(self))}>'

    def get_name(self) -> str:
        """
        :return: Returns a string containing the name of the plugin.
        """
        return self._name

    def get_path(self) -> str:
        """
        :retrurn: Returns the path towards the plugin folder containing the
         source code.
        """
        return join(self._path, self._name)

    def get_process(self) -> Popen:
        """
        :return: Returns the subprocess.Popen instance.
        """
        return self._process

    def get_specs(self) -> dict:
        """
        :return: Returns the plugin's manifest.json as a dictionary.
        """
        return self._specs

    def kill(self):
        """
        Force kill the plugin's process.

        In case of failure during an attempt to run the plugin, we force kill
        the process and set back 'self._process' to None.
        It ensures to properly restart the plugin after that.
        """
        if self._process is not None and isinstance(self._process, Popen):
            self._process.kill()
        self._process = None

    def restart(self):
        """
        Restart the plugin.

        We spawn a new process dedicated to this plugin and we store it into
        'self._process' to make it available and usable again.
        """
        if self._process is None:
            self._process = spawn(self)

    def shutdown(self):
        """
        Shutdown gracefully the plugin.

        In order to properly shutdown a plugin, we call the 'terminate()'
        method of the subprocess.Popen object and set back 'self.process' to
        None.
        """
        if self._process is not None and isinstance(self._process, Popen):
            self._process.terminate()
        self._process = None
