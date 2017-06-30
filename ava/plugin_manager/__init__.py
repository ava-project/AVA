import os, sys
from ..queues import QueuePlugin, QueueTtS
from ..components import _BaseComponent
from avasdk.plugins.ioutils.utils import *
from avasdk.exceptions import RuntimeError


class PluginManager(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.path = os.path.join(os.path.expanduser("~"), ".ava", "plugins")
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.process = {}
        self.plugins = {}
        self.plugins_disabled = []
        self.commands_for_a_specific_plugin = {}
        self.queue_plugin = QueuePlugin()
        self.queue_tts = QueueTtS()
        self._load_plugins()


    def _parse_plugins_folders(self, skip):
        """
        Handler for parsing every plugin folder and extract the name of the folder
        as the plugin name as well as the extension of the supplied files in order
        to determine in which language the plugin is written.
        It fills the dictionary 'self._plugins' with the plugin name as key and
        a JSON object as value.
        So far the JSON object has an element named 'lang' with the value a string
        containing the extension of the source code file of the plugin.

        for example, if we are using a plugin named 'hello_world' written in C++,
        the dictionary 'self._plugins' will look like following:

            {'hello_world': {'lang': 'cpp'}}

        @param:
            - skip: array of strings  (extension to skip i.e 'json')

        @behave:
            - raises an error if the specified directory does not exist.
        """
        if os.path.isdir(self.path) == False:
            raise RuntimeError(__name__, self._parse_plugins_folders.__name__, " Invalid path to the folder holding the plugins.")

        for directory in os.listdir(self.path):
            if self.plugins.get(directory) is not None:
                continue
            current_plugin_folder = os.path.join(self.path, directory)
            if os.path.isdir(current_plugin_folder) == True:
                for file in os.listdir(current_plugin_folder):
                    if file == 'setup.py':
                        continue
                    if file.find(".") > 0 and file[file.find(".") + 1:] not in skip:
                        self.plugins[directory] = {'lang': file[file.find(".") + 1:]}


    def _load_plugins(self):
        """
        Loads every plugin, caches the data and spawns a dedicated child process
        for each plugin with a 'Popen' object.
        Instances of the 'Popen' classes are stored in the dictionary 'self._process'
        with the name of the plugin as key and the corresponding instance of the 'Popen'
        class.
        """
        try:
            self._parse_plugins_folders(['json', 'txt', 'md'])

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])

        try:
            for key, value in self.plugins.items():
                if len(self.plugins[key]) > 1:
                    continue
                parse_json_file_to_dictionary(os.path.join(self.path, key), self.plugins[key])

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])


    def _extract_commands(self, skip):
        """
        Extracts each command name and its phonetic equivalent for a specific plugin.

            @return:
                Returns a dictionary formated as following {key, value} with:
                    - key: string (the commmand name)
                    - value: string (phonetic equivalent)
        """
        return {x: self.commands_for_a_specific_plugin[x] for x in self.commands_for_a_specific_plugin if x not in skip}


    def install(self, path):
        """
        Install a plugin from the given zip file by unziping and copying its content to the plugins folder.

            @param:
                - string (/path/to/the/zip/file)

            @behave:
                - raises an error if the object pointed by 'path' is not a valid zip file.
        """
        try:
            unzip(path, self.path)
            self._load_plugins()

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])


    def uninstall(self, plugin):
        """
        Uninstall a plugin by removing the plugin's folder and all its content.

            @param:
                - string (plugin to uninstall)
        """
        try:
            remove_directory(os.path.join(self.path, plugin))

        except RuntimeError as err:
            print(format_output(err.args[0], err.args[1]), err.args[2])
            return

        if self.plugins.get(plugin) is not None:
            self.plugins.pop(plugin, None)


    def enable(self, plugin):
        """
        Enables the specified plugin.

            @param:
                - plugin: string (the plugin name)

            @behave:
                - Plugins are enabled by default. Use this method if you want to
                enable a plugin which has been disabled by the 'disable' method.
        """
        if self.plugins.get(plugin) is None:
            return False
        if plugin in self.plugins_disabled:
            self.plugins_disabled.remove(plugin)
        return True


    def disable(self, plugin):
        """
        Disables the specified plugin.

            @param:
                - plugin: string(the plugin name)
        """
        if self.plugins.get(plugin) is not None:
            if plugin in self.plugins_disabled:
                pass
            else:
                self.plugins_disabled.append(plugin)
            return True
        return False


    def get_commands(self, plugin):
        """
        Returns a dictionary containing the commands for the specified plugin. Data are kept in memory.

            @param:
                -   plugin: string (the plugin name)

            @return:
                Returns None if there is no such plugin, otherwise a dictionary formated as following:
                {key, value} with key: string (the command name)
                                value: sring (the phonetic equivalent of the command)
        """
        if self.plugins.get(plugin) is None:
            return None

        if self.commands_for_a_specific_plugin.get('name') is not None and self.commands_for_a_specific_plugin['name'] == plugin:
                return self._extract_commands("name")

        self.commands_for_a_specific_plugin.clear()
        self.commands_for_a_specific_plugin['name'] = plugin
        for cmd in self.plugins[plugin]['commands']:
            self.commands_for_a_specific_plugin[cmd['name']] = cmd['phonetic']
        return self._extract_commands("name")


    def run(self):
        command = self.queue_plugin.get()
        print('Plugin manager execute : {}'.format(command))
        self.queue_tts.put('task completed')
        self.queue_plugin.task_done()
