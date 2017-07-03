import os
from subprocess import Popen, PIPE, STDOUT

def spawn_process(plugin):
    path = os.path.join('ava', 'process')
    # TODO improve the line 7
    target = plugin['commands'][0]['exec']
    handler = {
        'cpp': 'cpp_plugin_process.py',
        'go': 'golang_plugin_process.py',
    }.get(plugin['lang'], 'python_plugin_process.py')
    process = Popen(['python', os.path.join(path, handler), target], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    return process
