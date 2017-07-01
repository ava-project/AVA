from ..utils import Singleton
from subprocess import Popen, PIPE, STDOUT


class PluginStore(metaclass=Singleton):

    def __init__(self):
        self.plugins = {}
        self.process = {}
