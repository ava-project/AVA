import os, sys, json, importlib, subprocess

PLUGIN = {}

def main():
    """
    """
    name = sys.argv[1]
    import_module(name)
    while True:
        # TODO fix
        cmd = input('')
        execute(name, cmd)

def import_module(name):
    """
    """
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        manifest = json.load(json_file)
    if not PLUGIN.get(name):
        if 'build' in manifest and manifest['build'] == True:
            create_module(path, name)
        PLUGIN[name] = getattr(importlib.import_module(name), 'hello')

def create_module(path, name):
    """
    """
    setup = os.path.join(path, name, 'setup.py')
    subprocess.call(['python', setup, 'install'])

def execute(name, command):
    """
    """
    if PLUGIN.get(name):
        cmd = command.split(' ')
        plugin = PLUGIN.get(name)
        if cmd[0] in plugin.__dict__:
            plugin.__dict__[cmd[0]](plugin, ' '.join(cmd[1:]) if len(cmd) > 1 else '')
            return
        print('The plugin ', name, ' cannot handle the following command: ', cmd[0], flush=False)

if __name__ == "__main__":
    main()
