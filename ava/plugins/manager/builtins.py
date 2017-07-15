import os
from ..plugin import Plugin
from ..store import PluginStore
from avasdk.plugins.ioutils.utils import unzip, remove_directory

class PluginBuiltins(object):
    store = PluginStore()
    builtins = ['install', 'uninstall', 'enable', 'disable']

    @staticmethod
    def install(path_to_the_plugin_to_install):
        """
        """
        name = path_to_the_plugin_to_install
        name = name[:name.rfind('.zip')]
        name = name[1 + name.rfind(os.sep):]
        if PluginBuiltins.store.get_plugin(name):
            return 'The plugin ' + name + ' is already installed.'
        unzip(path_to_the_plugin_to_install, PluginBuiltins.store.path)
        PluginBuiltins.store.add_plugin(name, Plugin(name, PluginBuiltins.store.path))
        return 'Installation succeeded.'

    @staticmethod
    def uninstall(plugin_to_uninstall):
        """
        """
        PluginBuiltins.store.remove_plugin(plugin_to_uninstall)
        remove_directory(os.path.join(PluginBuiltins.store.path, plugin_to_uninstall))
        return 'Uninstalling the ' + plugin_to_uninstall + ' plugin succeeded.'

    @staticmethod
    def enable(plugin_to_enable):
        """
        """
        if not PluginBuiltins.store.get_plugin(plugin_to_enable):
            return 'No plugin named ' + plugin_to_enable + ' found.'
        if PluginBuiltins.store.is_plugin_disabled(plugin_to_enable):
            PluginBuiltins.store.enable_plugin(plugin_to_enable)
            return 'Plugin ' + plugin_to_enable + ' enabled.'
        else:
            return 'Plugin ' + plugin_to_enable + ' is already enabled.'

    @staticmethod
    def disable(plugin_to_disable):
        """
        """
        if not PluginBuiltins.store.get_plugin(plugin_to_disable):
            return 'No plugin named ' + plugin_to_disable + ' found.'
        if not PluginBuiltins.store.is_plugin_disabled(plugin_to_disable):
            PluginBuiltins.store.disable_plugin(plugin_to_disable)
            return 'Plugin ' + plugin_to_disable + ' disabled.'
        else:
            return 'Plugin ' + plugin_to_disable + ' is already disabled.'
