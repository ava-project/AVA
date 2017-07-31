import os
import pip
import sys
import json
import types
from importlib.machinery import SourceFileLoader
from avasdk.plugins.ioutils.utils import split_string

PLUGIN = {}

def import_module(plugin_name):
    """
    """
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", plugin_name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        manifest = json.load(json_file)
    if not PLUGIN.get(plugin_name):
        if 'build' in manifest and manifest['build'] == True:
            install_from_requirements(path)
        mod = SourceFileLoader(plugin_name, os.path.join(path, manifest['source'])).load_module()
        PLUGIN[plugin_name] = getattr(sys.modules[mod.__name__], plugin_name)
    print('__END_OF_IMPORT__')

def install_from_requirements(path):
    """
    """
    requirements = os.path.join(path, "requirements.txt")
    pip.main(['install', '-r', requirements])

def wait_for_command(plugin_name):
    """
    """
    while True:
        command = input('')
        if command == 'ping':
            print('pong')
            continue
        execute(plugin_name, command)
        print('__END_OF_RESPONSE__')

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
    try:
        plugin_name = sys.argv[1]
        import_module(plugin_name)
        wait_for_command(plugin_name)
    except Exception as err:
        print(err, file=sys.stderr)
        print(plugin_name + ' crashed. Restarting ...')
        print('__END_OF_RESPONSE__')
