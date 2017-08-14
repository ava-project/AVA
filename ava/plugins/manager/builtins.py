import os
from ..plugin import Plugin
from ..store import PluginStore
from avasdk.plugins.ioutils.utils import unzip, remove_directory

class PluginBuiltins(object):
    """Builtins handler.

    info:
        - All methods are static and must be used without instanciate this object.
    """

    store = PluginStore()
    builtins = ['install', 'uninstall', 'enable', 'disable']

    @staticmethod
    def install(path_to_the_plugin_to_install):
        """Install a plugin.
            Unzip the zipfile located at 'path_to_the_plugin_to_install' and add
            a new Plugin object to the store.

        param:
            - path_to_the_plugin_to_install: path to the zipfile containing the plugin source code (string).
        return:
            - Returns the status of the installation (string).
        """
        name = path_to_the_plugin_to_install
        name = name[:name.rfind('.zip')]
        name = name[1 + name.rfind(os.sep):]
        if PluginBuiltins.store.get_plugin(name):
            return 'The plugin {} is already installed.'.format(name)
        unzip(path_to_the_plugin_to_install, PluginBuiltins.store.path)
        PluginBuiltins.store.add_plugin(name, Plugin(name, PluginBuiltins.store.path))
        return 'Installation succeeded.'

    @staticmethod
    def uninstall(plugin_to_uninstall):
        """Uninstall the specified plugin.
            Removes all files located in $HOME/.ava/plugins/plugin_to_uninstall

        param:
            - plugin_to_uninstall: The name of the plugin to uninstall (string).
        return:
            - Returns the status of the uninstallation (string).
        """
        PluginBuiltins.store.remove_plugin(plugin_to_uninstall)
        remove_directory(os.path.join(PluginBuiltins.store.path, plugin_to_uninstall))
        return 'Uninstalling the {} plugin succeeded.'.format(plugin_to_uninstall)

    @staticmethod
    def enable(plugin_to_enable):
        """Enable the specified plugin.

        param:
            - plugin_to_enable: The name of the plugin to enable (string).
        return:
            - Returns the status of the activation (string).
        """
        if not PluginBuiltins.store.get_plugin(plugin_to_enable):
            return 'No plugin named {} found.'.format(plugin_to_enable)
        if PluginBuiltins.store.is_plugin_disabled(plugin_to_enable):
            PluginBuiltins.store.enable_plugin(plugin_to_enable)
            return 'Plugin {} enabled.'.format(plugin_to_enable)
        else:
            return 'Plugin {} is already enabled.'.format(plugin_to_enable)

    @staticmethod
    def disable(plugin_to_disable):
        """Disable the specified plugin.

        param:
            - plugin_to_disable: The name of the plugin to disable (string).
        return:
            - Returns the status of the deactivation (string).
        """
        if not PluginBuiltins.store.get_plugin(plugin_to_disable):
            return 'No plugin named {} found.'.format(plugin_to_disable)
        if not PluginBuiltins.store.is_plugin_disabled(plugin_to_disable):
            PluginBuiltins.store.disable_plugin(plugin_to_disable)
            return 'Plugin {} disabled.'.format(plugin_to_disable)
        else:
            return 'Plugin {} is already disabled.'.format(plugin_to_disable)
