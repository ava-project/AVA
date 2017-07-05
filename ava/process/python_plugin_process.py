import os, sys, json
from importlib.machinery import SourceFileLoader

PLUGIN = {}

def main():
    name = sys.argv[1]
    import_module(name)
    while True:
        cmd = sys.stdin.read()
        execute(name, cmd)

def import_module(name):
    path = os.path.join(os.path.expanduser("~"), ".ava", "plugins", name)
    with open(os.path.join(path, "manifest.json")) as json_file:
        data = json.load(json_file)
    if PLUGIN.get(name) is None:
        if 'build' in data:
            install_from_requirements(path)
        mod = SourceFileLoader(name, os.path.join(path, data['source'])).load_module()
        PLUGIN[name] = getattr(sys.modules[mod.__name__], name)

def install_from_requirements(path):
    requirements = os.path.join(path, "requirements.txt")
    pip.main(['install', '-r', requirements])

def execute(name, command):
    if PLUGIN.get(name) is not None:
        self_ = PLUGIN[name]
        print('name = ', name, ' command = ', command)
    else:
        print('An error occurred.')

if __name__ == "__main__":
    main()
