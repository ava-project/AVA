from threading import Lock
from os.path import join, expanduser
from ..plugin import Plugin
from ...utils import Singleton


class PluginStore(metaclass=Singleton):
    """
    A shared store of plugins.

    The PluginStore is a singleton offering the possibility to access plugins
    throughout the program.
    In order to guarantee the thread safety, you MUST use it only with the
    available methods. Using the instance variables directly can cause undefined
    behavior.
    """
    mutex = Lock()

    def __init__(self):
        self._path = join(expanduser('~'), '.ava', 'plugins')
        self._plugins = {}
        self._disabled = []

    def __repr__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>'

    def add_plugin(self, name: str, plugin: Plugin):
        """
        Add a new plugin to the store.

        :param name: The name of the new plugin (string).
        :param plugin: An instance of the new plugin (Plugin)
        """
        with PluginStore.mutex:
            if self._plugins.get(name) is None:
                self._plugins[name] = plugin

    def get_path(self) -> str:
        """
        :return: Returns the path towards the folder where the plugins are stored
         on the user's
        """
        return self._path

    def get_plugin(self, plugin: str) -> Plugin:
        """
        :param: plugin: The name of the plugin (string)

        :return: Whether None or the instance of the Plugin class if it is
         actually stored.
        """
        with PluginStore.mutex:
            return self._plugins.get(plugin)

    def get_plugins(self) -> dict:
        """
        :return: Returns the dictionary containing the instances of the plugins.
        """
        return self._plugins

    def get_a_detailed_list_of_plugins(self) -> list:
        """
        :return: Returns the list of the plugins installed. The name, version as
         well as a description are provided for each plugin.
        """
        plugins_list = []
        with PluginStore.mutex:
            for _, plugin in self._plugins.items():
                dictionary = {}
                dictionary['name'] = plugin.get_name()
                dictionary['version'] = plugin.get_specs()['version']
                dictionary['description'] = plugin.get_specs()['description']
                plugins_list.append(dictionary)
        return plugins_list

    def remove_plugin(self, plugin: str):
        """
        Removes the specified plugin from the store.

        :param plugin: The name of the plugin to remove (string).
        """
        with PluginStore.mutex:
            if self._plugins.get(plugin) is not None:
                self._plugins.pop(plugin, None).shutdown()

    def is_plugin_disabled(self, plugin: str) -> bool:
        """
        Returns True or False whether the specified plugin is disabled or not.

        :param plugin: The name of the plugin (string).

        :return: A boolean.
        """
        with PluginStore.mutex:
            return plugin in self._disabled

    def enable_plugin(self, plugin: str):
        """
        Enables the specified plugin.

        :param plugin: The name of the plugin to enable (string).
        """
        with PluginStore.mutex:
            self._disabled.remove(plugin)

    def disable_plugin(self, plugin: str):
        """
        Disables the specified plugin.

        :param plugin: The name of the plugin to disable (string).
        """
        with PluginStore.mutex:
            if plugin not in self._disabled:
                self._disabled.append(plugin)

    def clear(self):
        """
        Clears completely the store.

        In order to shutdown gracefully AVA, we clear the store by calling the
        shutdown method of each plugin stored. Finally we clear the dictionary
        of its entries.
        """
        with PluginStore.mutex:
            self._disabled = []
            for _, plugin in self._plugins.items():
                plugin.shutdown()
            self._plugins.clear()
