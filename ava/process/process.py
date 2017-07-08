import os
from subprocess import Popen, PIPE, STDOUT

class NotSupportedLanguage(Exception):
    pass


def spawn_process(plugin):
    """
    """
    path = os.path.join('ava', 'process')
    handler = {
        'cpp': 'cpp_plugin_process.py',
        'go': 'golang_plugin_process.py',
        'py': 'python_plugin_process.py',
    }.get(plugin['lang'], None)
    if not handler:
        raise NotSupportedLanguage('Error: Plugin language not supported.')
    # TODO fix binary name depending on the os
    process = Popen(['python', os.path.join(path, handler), plugin['name']], stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    return process
