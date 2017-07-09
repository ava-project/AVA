import os
from threading import Lock
from ...utils import Singleton

class PluginStore(metaclass=Singleton):
    mutex = Lock()

    def __init__(self):
        """Initializer

            @param: None
        """
        self.path = os.path.join(os.path.expanduser("~"), ".ava", "plugins")
        self.plugins = {}
        self.disabled = []

    def add_plugin(self, name, plugin):
        """
        """
        PluginStore.mutex.acquire()
        if self.plugins.get(name) is None:
            self.plugins[name] = plugin
        PluginStore.mutex.release()

    def get_plugin(self, plugin):
        """
        """
        PluginStore.mutex.acquire()
        result = self.plugins.get(plugin)
        PluginStore.mutex.release()
        return result

    def remove_plugin(self, plugin):
        """
        """
        PluginStore.mutex.acquire()
        if self.plugins.get(plugin) is not None:
            self.plugins.get(plugin).shutdown()
            self.plugins.pop(plugin, None)
        PluginStore.mutex.release()

    def is_plugin_disabled(self, plugin):
        """
        """
        result = False
        PluginStore.mutex.acquire()
        if plugin in self.disabled:
            result = True
        PluginStore.mutex.release()
        return result

    def enable_plugin(self, plugin):
        """
        """
        PluginStore.mutex.acquire()
        self.disabled.remove(plugin)
        PluginStore.mutex.release()

    def disable_plugin(self, plugin):
        """
        """
        PluginStore.mutex.acquire()
        self.disabled.append(plugin)
        PluginStore.mutex.release()
