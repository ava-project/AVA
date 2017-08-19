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
        self.plugin['interaction_required'] = False

    def plugin_requires_user_interaction(self, name):
        """
        """
        assert name is not None
        with State.plugin_state_mutex:
            self.plugin['name'] = name
            self.plugin['interaction_required'] = True

    def plugin_stops_waiting_for_user_interaction(self):
        """
        """
        with State.plugin_state_mutex:
            self.plugin['name'] = None
            self.plugin['interaction_required'] = False
        print('DEBUGDEBUG')

    def is_plugin_waiting_for_user_interaction(self):
        """
        """
        with State.plugin_state_mutex:
            return self.plugin['interaction_required'], self.plugin['name']
