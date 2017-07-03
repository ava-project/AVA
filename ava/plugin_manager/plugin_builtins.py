import os
from ..process import spawn_process
from ..plugin_store import PluginStore
from avasdk.plugins.ioutils.utils import unzip, remove_directory, load_plugin

class PluginBuiltins(object):
    store = PluginStore()

    @staticmethod
    def install(path_to_the_plugin_to_install):
        '''
        '''
        name = path_to_the_plugin_to_install
        name = name[:name.rfind('.zip')]
        name = name[1 + name.rfind(os.sep):]
        if PluginBuiltins.store.get_plugin(name):
            return 'The plugin ' + name + ' is already installed.'
        unzip(path_to_the_plugin_to_install, PluginBuiltins.store.path)
        plugin = load_plugin(PluginBuiltins.store.path, name)
        PluginBuiltins.store.add_plugin(name, plugin[name])
        process = spawn_process(plugin[name])
        PluginBuiltins.store.add_plugin_process(name, process)
        print('PluginStore process for: ', name, ' object: ', PluginBuiltins.store.get_plugin_process(name))
        print('PluginStore process for: ', name, ' pid: ', PluginBuiltins.store.get_plugin_process(name).pid)
        print('PluginStore process for: ', name, ' args: ', PluginBuiltins.store.get_plugin_process(name).args)
        print('PluginStore process for: ', name, ' stdout: ', PluginBuiltins.store.get_plugin_process(name).stdout.read())
        return 'Installation succeeded.'

    @staticmethod
    def uninstall(plugin_to_uninstall):
        '''
        '''
        PluginBuiltins.store.remove_plugin(plugin_to_uninstall)
        remove_directory(os.path.join(PluginBuiltins.store.path, plugin_to_uninstall))
        return 'Uninstalling the ' + plugin_to_uninstall + ' plugin succeeded.'

    @staticmethod
    def enable(plugin_to_enable):
        '''
        '''
        if PluginBuiltins.store.get_plugin(plugin_to_enable) is None:
            return 'No plugin named ' + plugin_to_enable + ' found.'
        if PluginBuiltins.store.is_plugin_disabled(plugin_to_enable):
            PluginBuiltins.store.enable_plugin(plugin_to_enable)
            return 'Plugin ' + plugin_to_enable + ' enabled.'
        else:
            return 'Plugin ' + plugin_to_enable + ' is already enabled.'

    @staticmethod
    def disable(plugin_to_disable):
        '''
        '''
        if PluginBuiltins.store.get_plugin(plugin_to_disable) is None:
            return 'No plugin named ' + plugin_to_disable + ' found.'
        if not PluginBuiltins.store.is_plugin_disabled(plugin_to_disable):
            PluginBuiltins.store.disable_plugin(plugin_to_disable)
            return 'Plugin ' + plugin_to_disable + ' disabled.'
        else:
            return 'Plugin ' + plugin_to_disable + ' is already disabled.'
