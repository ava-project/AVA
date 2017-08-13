import os
from threading import Lock
from ...utils import Singleton

class PluginStore(metaclass=Singleton):
    """A shared store holding all the plugin installed by the user.

        @info:
            - This object is a Singleton.
            - The provided methods of this object are thread safe.
    """
    mutex = Lock()

    def __init__(self):
        """Initializer

            @info:
                - DO NOT use these attributes directly. In order to ensure the
                thread safety of the store, please use the methods below.
        """
        self.path = os.path.join(os.path.expanduser("~"), ".ava", "plugins")
        self.plugins = {}
        self.disabled = []

    def add_plugin(self, name, plugin):
        """Add a new plugin to the store.

            @params:
                - name: the name of the new plugin (string).
                - plugin: an instance of the new plugin (Plugin)
        """
        with PluginStore.mutex:
            if self.plugins.get(name) is None:
                self.plugins[name] = plugin

    def get_plugin(self, plugin):
        """Allows to access to the instance of a specific plugin.

            @param:
                - plugin: the name of the plugin (string)

            @return:
                - (Plugin object) or None whether the specified plugin is currently stored.
        """
        result = None
        with PluginStore.mutex:
            result = self.plugins.get(plugin)
        return result

    def get_plugin_list(self):
        """Allows to retrieve a dictionary containg for each plugin stored, the name,
            the version as well as a description.

            @return:
                - dictionary.
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
        """Removes the specified plugin from the store.

            @param:
                - plugin: The name of the plugin to remove (string).
        """
        with PluginStore.mutex:
            if self.plugins.get(plugin) is not None:
                self.plugins.pop(plugin, None).shutdown()

    def is_plugin_disabled(self, plugin):
        """Returns True or False whether the specified plugin is disabled.

            @param:
                - plugin: The name of the plugin (string).

            @return:
                - boolean.
        """
        result = False
        with PluginStore.mutex:
            if plugin in self.disabled:
                result = True
        return result

    def enable_plugin(self, plugin):
        """Enables the specified plugin.

            @param:
                - plugin: The name of the plugin to enable (string).
        """
        with PluginStore.mutex:
            self.disabled.remove(plugin)

    def disable_plugin(self, plugin):
        """Disables the specified plugin.

            @param:
                - plugin: The name of the plugin to disable (string).
        """
        with PluginStore.mutex:
            self.disabled.append(plugin)

    def clear(self):
        """Clears completely the store.
        """
        with PluginStore.mutex:
            self.disabled = []
            for _, plugin in self.plugins:
                plugin.shutdown()
            self.plugins.clear()
