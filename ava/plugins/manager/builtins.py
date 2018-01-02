import os
# local imports
from ..plugin import Plugin
from ..store import PluginStore
# sdk
from avasdk.plugins.utils import unzip, remove_directory


class PluginBuiltins(object):
    """
    This class handles the specific 'builtins' for the plugins.

    The user is able to install, uninstall, enable or disable a plugin.
    Each method is preceded by the 'static' decorator, that means you do not
    need to instanciate the PluginBuiltins class to use them.
    """

    store = PluginStore()
    path = PluginStore().get_path()
    builtins = ['install', 'uninstall', 'enable', 'disable']

    @staticmethod
    def install(target: str) -> str:
        """
        Install a plugin.

        Unzip the zipfile located at 'target' and add
        a new Plugin object to the store.

        :param target: path to the zipfile containing the
         plugin source code (string).

        Returns:
            Returns the status of the installation (string).
        """
        name = target
        name = name[:name.rfind('.zip')]
        name = name[1 + name.rfind(os.sep):]
        if PluginBuiltins.store.get_plugin(name):
            return 'The plugin {} is already installed.'.format(name)
        unzip(target, PluginBuiltins.path)
        PluginBuiltins.store.add_plugin(name)
        return 'Installing the plugin {} succeeded.'.format(name)

    @staticmethod
    def uninstall(target: str) -> str:
        """
        Uninstall the specified plugin.

        Removes all files located in $HOME/.ava/plugins/target

        :param target: The name of the plugin to uninstall (string).

        :return: Returns the status of the uninstallation (string).
        """
        if not PluginBuiltins.store.get_plugin(target):
            return 'No plugin named {} found'.format(target)
        PluginBuiltins.store.remove_plugin(target)
        remove_directory(os.path.join(PluginBuiltins.path, target))
        return 'Uninstalling the plugin {} succeeded.'.format(target)

    @staticmethod
    def enable(target: str) -> str:
        """
        Enable the requested plugin.

        :param target: The name of the plugin to enable (string).

        :return: Returns the status of the activation (string).
        """
        if not PluginBuiltins.store.get_plugin(target):
            return 'No plugin named {} found.'.format(target)
        if not PluginBuiltins.store.is_plugin_disabled(target):
            return 'The plugin {} is already enabled.'.format(target)
        PluginBuiltins.store.enable_plugin(target)
        return 'The plugin {} has been enabled.'.format(target)

    @staticmethod
    def disable(target: str) -> str:
        """
        Disable the specified plugin.

        :param target: The name of the plugin to disable (string).

        :return: Returns the status of the deactivation (string).
        """
        if not PluginBuiltins.store.get_plugin(target):
            return 'No plugin named {} found.'.format(target)
        if PluginBuiltins.store.is_plugin_disabled(target):
            return 'The plugin {} is already disabled.'.format(target)
        PluginBuiltins.store.disable_plugin(target)
        return 'The plugin {} has been disabled.'.format(target)
