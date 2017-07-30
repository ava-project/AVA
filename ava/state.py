from threading import Lock
from .utils import Singleton

class State(metaclass=Singleton):
    """
    """
    plugin_state_mutex = Lock()

    def __init__(self):
        """
        """
        self.plugin = {}
        self.plugin['name'] = None
        self.plugin['state'] = False


    def get_plugin_state(self):
        """
        """
        with State.plugin_state_mutex:
            return self.plugin['name'], self.plugin['state']

    def set_plugin_state(self, name=None):
        """
        """
        with State.plugin_state_mutex:
            self.plugin['name'] = name
            self.plugin['state'] = True if name else False
