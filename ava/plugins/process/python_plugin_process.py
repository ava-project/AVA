import os
import pip
import sys
import json
import types
from importlib.machinery import SourceFileLoader
from avasdk.plugins.ioutils.utils import split_string


PLUGIN = {}

def main():
    """
    """
    plugin_name = sys.argv[1]
    import_module(plugin_name)
    while True:
        # TODO fix
        command = input('')
        execute(plugin_name, command)

def import_module(plugin_name):
    """
    """
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", plugin_name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        manifest = json.load(json_file)
    if not PLUGIN.get(plugin_name):
        if 'build' in manifest and manifest['build'] == True:
            install_from_requirements(path)
        # TODO check
        mod = SourceFileLoader(plugin_name, os.path.join(path, manifest['source'])).load_module()
        PLUGIN[plugin_name] = getattr(sys.modules[mod.__name__], plugin_name)

# def import_module(plugin_name):
#     """
#     """
#     path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", plugin_name)
#     with open(os.path.join(path, "manifest.json")) as json_file:
#         manifest = json.load(json_file)
#     if not PLUGIN.get(plugin_name):
#         if 'build' in manifest and manifest['build'] == True:
#             print("DEBUG")
#             install_from_requirements(path)
#         # TODO check
#         loader = SourceFileLoader(plugin_name, os.path.join(path, manifest['source']))
#         print(loader)
#         print(loader.name)
#         mod = types.ModuleType(loader.name)
#         print(mod)
#         print(mod.__dict__)
#         loader.exec_module(mod)
#         print(loader)
        # PLUGIN[plugin_name] = getattr(sys.modules[plugin_name], plugin_name)



def install_from_requirements(path):
    """
    """
    requirements = os.path.join(path, "requirements.txt")
    pip.main(['install', '-r', requirements])

def execute(plugin_name, command):
    """
    """
    if PLUGIN.get(plugin_name):
        command_name, args = split_string(command, ' ')
        plugin = PLUGIN.get(plugin_name)
        if command_name in plugin.__dict__:
            plugin.__dict__[command_name](plugin, args if args else None)
            return
        print('The plugin ' +  plugin_name + ' cannot handle the following command: ' + command_name, flush=False)

if __name__ == "__main__":
    main()
