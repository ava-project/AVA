import os
from ..plugin_store import PluginStore
from avasdk.plugins.ioutils.utils import unzip, remove_directory

class PluginBuiltins(object):
    store = PluginStore()

    @staticmethod
    def install(path_to_the_plugin_to_install):
        '''
        '''
        try:
            unzip(path_to_the_plugin_to_install, PluginBuiltins.store.path)
            PluginBuiltins.store._load_plugins()
        except Exception as err:
            return str(err)
        return 'Installation succeeded.'


    @staticmethod
    def uninstall(plugin_to_uninstall):
        '''
        '''
        try:
            remove_directory(os.path.join(PluginBuiltins.store.path, plugin_to_uninstall))
        except Exception as err:
            return str(err)
        PluginBuiltins.store.remove_plugin(plugin_to_uninstall)
        return 'Uninstalling the ' + plugin_to_uninstall + ' plugin succeeded.'


    @staticmethod
    def enable(plugin_to_enable):
        '''
        '''
        if PluginBuiltins.store.get_plugin(plugin_to_enable) is None:
            return 'No plugin named ' + plugin_to_enable + ' found.'
        if PluginBuiltins.store.is_plugin_disabled(plugin_to_enable):
            PluginBuiltins.store.remove_disabled_plugin(plugin_to_enable)
        else:
            return 'Plugin ' + plugin_to_enable + ' is already enabled.'
        return 'Plugin ' + plugin_to_enable + ' enabled.'

    @staticmethod
    def disable(plugin_to_disable):
        '''
        '''
        if PluginBuiltins.store.get_plugin(plugin_to_disable) is not None:
            if not PluginBuiltins.store.is_plugin_disabled(plugin_to_disable):
                PluginBuiltins.store.disable_plugin(plugin_to_disable)
                return 'Plugin ' + plugin_to_disable + ' disabled.'
            else:
                return 'Plugin ' + plugin_to_disable + ' is already disabled.'
        return 'No plugin named ' + plugin_to_disable + ' found.'
