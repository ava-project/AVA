import os
from threading import Lock
from ...utils import Singleton


class PluginStore(metaclass=Singleton):
    """A shared store of plugins.

    The PluginStore is a singleton offering the possibility to access plugins
    throughout the program.
    In order to guarantee the thread safety, you MUST use it only with the
    available methods. Using the instance variables directly can cause undefined
    behavior.
    """
    mutex = Lock()

    def __init__(self):
        """Initializer.

        Initializing instance variables:
            self.path: Path to the user's folder where the plugins are installed.
            self.plugins: A dictionary formed with the key representing the name
                of the plugin and as a value the instance of the Plugin class.
            self.disabled: Array with the name of the plugin disabled.
        """
        self.path = os.path.join(os.path.expanduser("~"), ".ava", "plugins")
        self.plugins = {}
        self.disabled = []

    def add_plugin(self, name, plugin):
        """Add a new plugin to the store.

        Args:
            name: The name of the new plugin (string).
            plugin: An instance of the new plugin (Plugin)
        """
        with PluginStore.mutex:
            if self.plugins.get(name) is None:
                self.plugins[name] = plugin

    def get_plugin(self, plugin):
        """Returns the instance of the requested plugin.

        Args:
            plugin: The name of the plugin (string)

        Returns:
            Whether None or the instance of the Plugin class if it is
            actually stored.
        """
        with PluginStore.mutex:
            return self.plugins.get(plugin)

    def get_plugin_list(self):
        """A list of elements containing each the name of a plugin, its version
        as well as its desciption formated in a dictionary.

        Returns:
            The list of all plugins stored.
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

        param:
            - plugin: The name of the plugin to remove (string).
        """
        with PluginStore.mutex:
            if self.plugins.get(plugin) is not None:
                self.plugins.pop(plugin, None).shutdown()

    def is_plugin_disabled(self, plugin):
        """Returns True or False whether the requested plugin is disabled.

        Args:
            plugin: The name of the plugin (string).

        Returns:
            A boolean.
        """
        with PluginStore.mutex:
            return plugin in self.disabled

    def enable_plugin(self, plugin):
        """Enables the requested plugin.

        Args:
            plugin: The name of the plugin to enable (string).
        """
        with PluginStore.mutex:
            self.disabled.remove(plugin)

    def disable_plugin(self, plugin):
        """Disables the requested plugin.

        Args:
            plugin: The name of the plugin to disable (string).
        """
        with PluginStore.mutex:
            self.disabled.append(plugin)

    def clear(self):
        """Clears completely the store.

        In order to shutdown gracefully AVA, we clear the store by calling the
        shutdown method of each plugin stored. Finally we clear the dictionary
        of its entries.
        """
        with PluginStore.mutex:
            self.disabled = []
            for _, plugin in self.plugins.items():
                plugin.shutdown()
            self.plugins.clear()
