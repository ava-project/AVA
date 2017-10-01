import os
import sys
import json
from importlib.machinery import SourceFileLoader
from avasdk.plugins.utils import split_string
from avasdk.plugins.log import Logger

PLUGIN = {
    'cpp': {},
    'go': {},
    'py': {}
}
LANG = None

def import_module(plugin_name):
    """Import a module in runtime.

    param:
        - plugin_name: The name of the module to import (string).
    """
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", plugin_name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        manifest = json.load(json_file)
    assert manifest is not None and 'source' in manifest
    if not PLUGIN[LANG].get(plugin_name):
        if 'build' in manifest and manifest['build'] == True:
            builder(path)
        loader(plugin_name, path, manifest)
    Logger.log_import()

def builder(path):
    """
    """
    if LANG == 'cpp':
        import subprocess
        subprocess.call(['python', os.path.join(path, 'setup.py'), 'install'])
    elif LANG == 'py':
        import pip
        pip.main(['install', '-r', os.path.join(path, "requirements.txt")])
    elif LANG == 'go':
        from ctypes import cdll
        print(cdll)

def loader(target, path, manifest):
    """
    """
    if LANG == 'cpp':
        PLUGIN[LANG][target] = {}
        for command in manifest['commands']:
            PLUGIN[LANG][target][command['target']] = getattr(
                importlib.import_module(target), command['name'])
    else:
        src = SourceFileLoader(target, os.path.join(path, manifest['source']))
        mod = src.load_module()
        PLUGIN[LANG][target] = getattr(sys.modules[mod.__name__], target)

def wait_for_command(plugin_name):
    """Wait for an input from the user.

    param:
        - plugin_name: The name of the plugin waiting for an user's input.
    """
    while True:
        execute(plugin_name, input())
        Logger.log_response()


def execute(plugin_name, command):
    """Execute the given command of the plugin named 'plugin_name'

    params:
        - plugin_name: The name of the plugin running (string).
        - command: the user's input (string).
    """
    if PLUGIN[LANG].get(plugin_name):
        plugin = PLUGIN[LANG].get(plugin_name)
        command_name, args = split_string(command, ' ')
        if LANG == 'cpp':
            if plugin.get(command_name):
                print(plugin[command_name](args if args else ''))
                return
        else:
            if command_name in plugin.__dict__:
                plugin.__dict__[command_name](plugin, args if args else None)
                return
        print('The plugin {} cannot handle the following command: {}'.format(
                    plugin_name, command_name), flush=False)
    else:
        raise RuntimeError('Unexpected error occured.')


if __name__ == "__main__":
    try:
        plugin_name = sys.argv[1]
        LANG = sys.argv[2]
        import_module(plugin_name)
        wait_for_command(plugin_name)
    except:
        import traceback
        traceback.print_exc(file=sys.stdout)
        Logger.log_error()
