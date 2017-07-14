import os, sys, json, importlib, subprocess
from avasdk.plugins.ioutils.utils import split_string

PLUGIN = {}

def import_module(name):
    """
    """
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        manifest = json.load(json_file)
    if not PLUGIN.get(name):
        if 'build' in manifest and manifest['build'] == True:
            create_module(path)
        PLUGIN[name] = {}
        for command in manifest['commands']:
            PLUGIN[name][command['name']] = getattr(importlib.import_module(name), command['name'])
    print('END_OF_IMPORT')

def create_module(path):
    """
    """
    setup = os.path.join(path, 'setup.py')
    subprocess.call(['python', setup, 'install'])

def wait_for_command(plugin_name):
    """
    """
    while True:
        # TODO fix
        command = input('')
        if command == 'ping':
            print('pong')
            continue
        execute(plugin_name, command)
        print('END_OF_COMMAND')

def execute(name, command):
    """
    """
    if PLUGIN.get(name):
        plugin = PLUGIN.get(name)
        func, args = split_string(command, ' ')
        if plugin.get(func):
            print(plugin[func](args if args else ''))
            return
        print('The plugin ', name, ' cannot handle the following command: ', func, flush=False)

if __name__ == "__main__":
    try:
        plugin_name = sys.argv[1]
        import_module(plugin_name)
        wait_for_command(plugin_name)
    except Exception as err:
        print(err, file=sys.stderr)
        print(plugin_name + ' crashed. Restarting ...')
        print('END_OF_COMMAND')
