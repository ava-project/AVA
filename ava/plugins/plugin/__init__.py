import os
import sys
import platform
import subprocess
# SDK
from avasdk.plugins.utils import load_plugin


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
        self._process = self._create_venv_and_process()

    def __repr__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__name__}.{self._name.capitalize()} at {hex(id(self))}>'

    def _create_venv_and_process(self) -> subprocess.Popen:
        """
        Creates a virtualenv and executes the plugin in a new process.

        :param plugin: The plugin instance.
        :return: The new process (subprocess.Popen), None if it fails.
        """
        name = self._name
        lang = self._specs['lang']
        path = os.path.join(os.environ['AVAPATH'], 'ava', 'plugins', 'context')
        if lang not in ['cpp', 'go', 'py']:
            raise NotSupportedLanguage('Plugin language not supported.')
        if platform.system() == 'Windows':
            venv_executable = 'venv/Scripts/python.exe'
        else:
            venv_executable = 'venv/bin/python3'
        py_venv = os.path.join(
            os.path.expanduser('~'), '.ava', 'plugins', name, venv_executable)
        if sys.executable is None:
            print(sys.executable)
            raise RuntimeError('Could not find a python interpreter')
        subprocess.call(
            [os.environ['PYTHONPATH'],
             os.path.join(path, 'venv.py'), name], stdout=None)
        return subprocess.Popen(
            [py_venv, os.path.join(path, 'main.py'), name, lang],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            universal_newlines=True)

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
        return os.path.join(self._path, self._name)

    def get_process(self) -> subprocess.Popen:
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
        if self._process and isinstance(self._process, subprocess.Popen):
            self._process.kill()
        self._process = None

    def restart(self):
        """
        Restart the plugin.

        We spawn a new process dedicated to this plugin and we store it into
        'self._process' to make it available and usable again.
        """
        if self._process is None:
            from ..utils import State
            State().is_restarting(self._name)
            self._process = self._create_venv_and_process()
            State().has_restarted(self._name)

    def shutdown(self):
        """
        Shutdown gracefully the plugin.

        In order to properly shutdown a plugin, we call the 'terminate()'
        method of the subprocess.Popen object and set back 'self.process' to
        None.
        """
        if self._process and isinstance(self._process, subprocess.Popen):
            self._process.terminate()
        self._process = None
