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
        with PluginStore.mutex:
            if self.plugins.get(name) is None:
                self.plugins[name] = plugin

    def get_plugin(self, plugin):
        """
        """
        result = None
        with PluginStore.mutex:
            result = self.plugins.get(plugin)
        return result

    def get_plugin_list(self):
        """
        """
        plugin_list = []
        with PluginStore.mutex:
            for field, plugin in self.plugins.items():
                dictionary = {}
                dictionary['name'] = plugin.get_name()
                dictionary['version'] = plugin.get_specs()['version']
                dictionary['description'] = plugin.get_specs()['description']
                plugin_list.append(dictionary)
        return plugin_list

    def remove_plugin(self, plugin):
        """
        """
        with PluginStore.mutex:
            if self.plugins.get(plugin) is not None:
                self.plugins.pop(plugin, None).shutdown()

    def is_plugin_disabled(self, plugin):
        """
        """
        result = False
        with PluginStore.mutex:
            if plugin in self.disabled:
                result = True
        return result

    def enable_plugin(self, plugin):
        """
        """
        with PluginStore.mutex:
            self.disabled.remove(plugin)

    def disable_plugin(self, plugin):
        """
        """
        with PluginStore.mutex:
            self.disabled.append(plugin)

    def clear(self):
        """
        """
        with PluginStore.mutex:
            for _, plugin in self.plugins:
                plugin.shutdown()
            self.plugins.clear()
