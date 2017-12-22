from os import path
from .process import spawn
# from ..state import State
# from ..loading import loading
from avasdk.plugins.utils import load_plugin


class Plugin(object):
    """Object representation of a plugin."""

    def __init__(self, name, path):
        """Initializer

        We load the plugin's manifest and spawn a process in which the execution
        of the plugin will be contained.

        Args:
            name: the plugin name (string).
            path: the path towards the plugin folder containing the plugin
                source code (string).
        """
        self.name = name
        self.path = path
        self.specs = load_plugin(self.path, self.name)[self.name]
        self.process = spawn(self)

    def get_name(self):
        """Returns the name of the plugin.

        Returns:
            A string containing the name of the plugin.
        """
        return self.name

    def get_path(self):
        """Returns the path towards the plugin folder containing the source code.

        Returns:
            The path to the plugin's source code.
        """
        return path.join(self.path, self.name)

    def get_process(self):
        """Returns the process in wich the plugin is executed.

        Returns:
            The subprocess.Popen instance.
        """
        return self.process

    def get_specs(self):
        """Returns the plugin specifications.

        Returns:
            The plugin's manifest.json as dictionary.
        """
        return self.specs

    def kill(self):
        """Force kill the plugin's process.

        In case of failure during an attempt to run the plugin, we force kill
        the process and set back 'self.process' to None.
        It ensures to properly restart the plugin after that.
        """
        assert self.process is not None
        self.process.kill()
        self.process = None

    def restart(self):
        """Restart the plugin.

        We spawn a new process dedicated to this plugin and we store it into
        'self.process' to make it available and usable again.
        """
        assert self.process is None
        # State().loading()
        # loading(plugins_nbr=1, process_time=6, target=self.name)
        self.process = spawn(self)
        # State().loading_done()

    def shutdown(self):
        """Shutdown the plugin gracefully.

        In order to properly shutdown each plugin, we call the 'terminate()'
        method of the subprocess.Popen object and set back 'self.process' to
        None.
        """
        assert self.process is not None
        self.process.terminate()
        self.process = None
