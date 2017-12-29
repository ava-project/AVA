import threading
from .utils import Singleton


class State(metaclass=Singleton):
    """
    """
    plugin_state_mutex = threading.Lock()
    loading_state_mutex = threading.Lock()

    def __init__(self):
        """
        """
        self.plugin = {}
        self.loading = True
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

    def is_plugin_waiting_for_user_interaction(self):
        """
        """
        with State.plugin_state_mutex:
            return self.plugin['interaction_required'], self.plugin['name']

    def is_loading(self):
        """
        """
        with State.loading_state_mutex:
            return self.loading

    def loading(self):
        """
        """
        with State.loading_state_mutex:
            self.loading = True

    def loading_done(self):
        """
        """
        with State.loading_state_mutex:
            self.loading = False
