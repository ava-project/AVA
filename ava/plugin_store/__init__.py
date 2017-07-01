import os
from threading import Lock
from ..utils import Singleton
from subprocess import Popen, PIPE, STDOUT
from avasdk.plugins.ioutils.utils import parse_json_file_to_dictionary


class PluginStore(metaclass=Singleton):
    mutex = Lock()

    def __init__(self):
        '''
        Initializer

            @param: None
        '''
        self.path = os.path.join(os.path.expanduser("~"), ".ava", "plugins")
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.plugins = {}
        self.process = {}
        self.disabled = []
        self._load_plugins()

    def _parse_plugins_folders(self, skip):
        '''
        Handler for parsing every plugin folder and extract the name of the folder
        as the plugin name as well as the extension of the supplied files in order
        to determine in which language the plugin is written.
        It fills the dictionary 'self.plugins' with the plugin name as key and a
        JSON object as value.
        So far the JSON object has an element named 'lang' with the value a string
        containing the extension of the source code file of the plugin.

        for example, if we are using a plugin named 'hello_world' written in C++,
        the dictionary 'self.plugins' will look like following:

            {'hello_world': {'lang': 'cpp'}}

        @param:
            - skip: array of strings  (extension to skip i.e 'json')
        '''
        for directory in os.listdir(self.path):
            if self.plugins.get(directory) is not None:
                continue
            current_plugin_folder = os.path.join(self.path, directory)
            if os.path.isdir(current_plugin_folder):
                for file in os.listdir(current_plugin_folder):
                    if file == 'setup.py':
                        continue
                    if file.find(".") > 0 and file[file.find(".") + 1:] not in skip:
                        self.plugins[directory] = {'lang': file[file.find(".") + 1:]}


    def _load_plugins(self):
        '''
        Loads every plugin, caches the data and spawns a dedicated child process
        for each plugin.
        '''
        self._parse_plugins_folders(['json', 'md', 'txt'])
        try:
            for key, value in self.plugins.items():
                if len(self.plugins[key]) > 1:
                    continue
                parse_json_file_to_dictionary(os.path.join(self.path, key), self.plugins[key])
        except Exception as err:
            print(str(err))


    def get_plugin(self, plugin):
        '''
        '''
        PluginStore.mutex.acquire()
        result = self.plugins.get(plugin)
        PluginStore.mutex.release()
        return result


    def remove_plugin(self, plugin):
        '''
        '''
        PluginStore.mutex.acquire()
        if self.plugins.get(plugin) is not None:
            self.plugins.pop(plugin, None)
        PluginStore.mutex.release()


    def is_plugin_disabled(self, plugin):
        '''
        '''
        result = False
        PluginStore.mutex.acquire()
        if plugin in self.disabled:
            result = True
        PluginStore.mutex.release()
        return result


    def remove_disabled_plugin(self, plugin):
        '''
        '''
        PluginStore.mutex.acquire()
        if plugin in self.disabled:
            self.disabled.remove(plugin)
        PluginStore.mutex.release()


    def disable_plugin(self, plugin):
        '''
        '''
        PluginStore.mutex.acquire()
        self.disabled.append(plugin)
        PluginStore.mutex.release()
