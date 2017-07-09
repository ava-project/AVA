from os import path
from .process import spawn_process
from avasdk.plugins.ioutils.utils import load_plugin

class Plugin(object):
    """ Object representation of a plugin. """

    def __init__(self, name, path):
        """Initializer

            @param:
                name: the plugin name (string)
        """
        self.name = name
        self.path = path
        self.process = None
        self.specs = {}
        self._init()

    def _init(self):
        """
        """
        self.specs = load_plugin(self.path, self.name)[self.name]
        self.process = spawn_process(self.specs)

    def get_name(self):
        """
        """
        return self.name

    def get_path(self):
        """
        """
        return path.join(self.path, self.name)

    def get_process(self):
        """
        """
        return self.process

    def get_specs(self):
        """
        """
        return self.specs

    def restart(self):
        """
        """
        self.process = spawn_process(self.specs)

    def shutdown(self):
        """
        """
        self.process.kill()
        self.process = None
