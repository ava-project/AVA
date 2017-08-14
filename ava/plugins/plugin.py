from os import path
from .process import spawn
from avasdk.plugins.ioutils.utils import load_plugin

class Plugin(object):
    """Object representation of a plugin."""

    def __init__(self, name, path):
        """Initializer

        params:
            - name: the plugin name (string).
            - path: the path towards the plugin folder containing the plugin source code (string).
        """
        self.name = name
        self.path = path
        try:
            self.specs = load_plugin(self.path, self.name)[self.name]
            self.process = spawn(self)
        except:
            raise

    def get_name(self):
        """Returns a string with the name of the plugin.

        return:
            - string.
        """
        return self.name

    def get_path(self):
        """Returns a string with the path towards the plugin folder containing the plugin source code.

        return
            - string.
        """
        return path.join(self.path, self.name)

    def get_process(self):
        """Returns the process in wich the plugin is executed.

        return
            - subprocess.Popen object.
        """
        return self.process

    def get_specs(self):
        """Returns a dictionary containing all the plugin specifications extracted
            from its manifest.json.

            @return:
                - dictionary.
        """
        return self.specs

    def kill(self):
        """Kill the plugin by killing its process. The subprocess.Popen object is set back to None."""
        try:
            self.process.stdin.close()
            self.process.stdout.close()
            self.process.kill()
            self.process = None
        except:
            raise

    def restart(self):
        """Restart the plugin by spawning a new dedicated processs."""
        assert self.process is None
        try:
            self.process = spawn(self)
        except:
            raise

    def shutdown(self):
        """Shutdown the plugin gracefully."""
        try:
            self.process.stdin.close()
            self.process.stdout.close()
            self.process.terminate()
            self.process = None
        except:
            raise
