import os
import pip
import sys
import json
from importlib.machinery import SourceFileLoader
from avasdk.plugins.ioutils.utils import split_string
from avasdk.plugins.log import ERROR, IMPORT, RESPONSE, DELIMITER, log

PLUGIN = {}

def import_module(plugin_name):
    """Import a module in runtime.

    param:
        - plugin_name: The name of the module to import (string).
    """
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", plugin_name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        manifest = json.load(json_file)
    assert manifest is not None and 'source' in manifest
    if not PLUGIN.get(plugin_name):
        if 'build' in manifest and manifest['build'] == True:
            install_from_requirements(path)
        mod = SourceFileLoader(plugin_name, os.path.join(path, manifest['source'])).load_module()
        PLUGIN[plugin_name] = getattr(sys.modules[mod.__name__], plugin_name)
    log(importing=True)

def install_from_requirements(path):
    """Install requirements from the 'requirements.txt' file located at path.

    param:
        - path: the path to the requirements.txt file (string).
    """
    requirements = os.path.join(path, "requirements.txt")
    pip.main(['install', '-r', requirements])

def wait_for_command(plugin_name):
    """Wait for an input from the user.

    param:
        - plugin_name: The name of the plugin waiting for an user's input.
    """
    while True:
        execute(plugin_name, input())
        log(response=True)

def execute(plugin_name, command):
    """Execute the given command of the plugin named 'plugin_name'

    params:
        - plugin_name: The name of the plugin running (string).
        - command: the user's input (string).
    """
    if PLUGIN.get(plugin_name):
        command_name, args = split_string(command, ' ')
        plugin = PLUGIN.get(plugin_name)
        if command_name in plugin.__dict__:
            plugin.__dict__[command_name](plugin, args if args else None)
            return
        print('The plugin {} cannot handle the following command: {}'.format(plugin_name, command_name), flush=False)
    else:
        raise RuntimeError('Unexpected error occured.')


if __name__ == "__main__":
    try:
        plugin_name = sys.argv[1]
        import_module(plugin_name)
        wait_for_command(plugin_name)
    except:
        log(error=True)
