import os, sys, json, io
# TODO check
from importlib.machinery import SourceFileLoader

PLUGIN = {}

def main():
    """
    """
    name = sys.argv[1]
    import_module(name)
    while True:
        # TODO fix
        cmd = sys.stdin.buffer.read()
        execute(name, cmd)

def import_module(name):
    """
    """
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        manifest = json.load(json_file)
    if not PLUGIN.get(name):
        if 'build' in manifest:
            install_from_requirements(path)
        # TODO check
        mod = SourceFileLoader(name, os.path.join(path, manifest['source'])).load_module()
        PLUGIN[name] = getattr(sys.modules[mod.__name__], name)

def install_from_requirements(path):
    """
    """
    requirements = os.path.join(path, "requirements.txt")
    pip.main(['install', '-r', requirements])

def execute(name, command):
    """
    """
    if PLUGIN.get(name):
        cmd = command.split(' ')
        plugin = PLUGIN.get(name)
        if cmd[0] in plugin.__dict__:
            print(plugin.__dict__[cmd[0]](plugin, str(' '.join(cmd[1:])) if len(cmd) > 1 else ''))
            return
        print('The plugin ', name, ' cannot handlle the following command: ', cmd[0])

if __name__ == "__main__":
    main()
