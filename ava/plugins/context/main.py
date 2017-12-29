import os
import sys
import json
from avasdk.plugins.log import Logger
from avasdk.plugins.utils import split_string
from importlib.machinery import SourceFileLoader

PLUGIN = {'cpp': {}, 'go': {}, 'py': {}}
LANG = None


def import_module(plugin_name: str):
    """
    Import a module in runtime.

    :param plugin_name: The name of the module to import (string).
    """
    path = os.path.join(
        os.path.expanduser('~'), '.ava', 'plugins', plugin_name)
    with open(os.path.join(path, 'manifest.json')) as json_file:
        manifest = json.load(json_file)
    assert manifest is not None and 'source' in manifest
    if not PLUGIN[LANG].get(plugin_name):
        if 'build' in manifest and manifest['build'] == True:
            builder(path, plugin_name)
        loader(plugin_name, path, manifest)
    Logger.log_import()


# TODO improve builder
def builder(path: str, plugin_name: str):
    """
    """
    if LANG == 'cpp':
        import subprocess
        subprocess.call(['python', os.path.join(path, 'setup.py'), 'install'])
    elif LANG == 'py':
        import pip
        pip.main(['install', '-r', os.path.join(path, "requirements.txt")])
    elif LANG == 'go':
        import subprocess
        subprocess.call([
            'go', 'build', '-buildmode=c-shared', '-o', '{}/{}.so'.format(
                path, plugin_name), '{}/{}.go'.format(path, plugin_name)
        ])


# TODO improve loader
def loader(target: str, path: str, manifest: dict):
    """
    """
    if LANG == 'cpp':
        import importlib
        PLUGIN[LANG][target] = {}
        for command in manifest['commands']:
            PLUGIN[LANG][target][command['name']] = getattr(
                importlib.import_module(target), command['name'])
    elif LANG == 'go':
        from ctypes import cdll
        PLUGIN[LANG][target] = cdll.LoadLibrary(
            '{}/{}.so'.format(path, target))
    else:
        src = SourceFileLoader(target, os.path.join(path, manifest['source']))
        mod = src.load_module()
        PLUGIN[LANG][target] = getattr(sys.modules[mod.__name__], target)


def wait_for_command(plugin_name: str):
    """
    Wait for an input from the user.

    :param plugin_name: The name of the plugin waiting for an user's input.
    """
    while True:
        execute(plugin_name, input())
        Logger.log_response()


# TODO improve execution
def execute(plugin_name: str, command: str):
    """
    Execute the given command of the plugin named 'plugin_name'

    :param plugin_name: The name of the plugin running (string).
    :param command: the user's input (string).
    """
    if PLUGIN[LANG].get(plugin_name):
        plugin = PLUGIN[LANG].get(plugin_name)
        command_name, args = split_string(command, ' ')
        if LANG == 'cpp':
            if plugin.get(command_name):
                print(plugin[command_name](args if args else ''))
                return
        elif LANG == 'go':
            func = getattr(plugin, command_name, None)
            if func is not None:
                func(args if args else '')
                return
        else:
            if command_name in plugin.__dict__:
                plugin.__dict__[command_name](plugin, args if args else None)
                return
        print(
            'The plugin {} cannot handle the following command: {}'.format(
                plugin_name, command_name),
            flush=False)
    else:
        raise RuntimeError('Unexpected error occured.')


if __name__ == "__main__":
    try:
        print('debug')
        plugin_name = sys.argv[1]
        LANG = sys.argv[2]
        import_module(plugin_name)
        wait_for_command(plugin_name)
    except:
        import traceback
        traceback.print_exc(file=sys.stdout)
        Logger.log_error()
