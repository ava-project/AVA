import os
import sys
import datetime
from subprocess import Popen, PIPE, STDOUT

class NotSupportedLanguage(Exception):
    pass


def ping_process(process):
    """
    """
    try:
        process.stdin.write('ping\n')
        process.stdin.flush()
        ret = process.stdout.readline().rstrip()
        return True if ret == 'pong' else False
    except Exception:
        return False

def flush_process_output(process, token):
    """
    """
    output = []
    while True:
        line = process.stdout.readline().rstrip()
        if line == token:
            break
        output.append(line)
    return output

def spawn_process(plugin):
    """
    """
    name = plugin.get_name()
    lang = plugin.get_specs()['lang']
    path = os.path.join('ava', 'plugins', 'process')
    handler = {
        'cpp': 'cpp_main',
        'py': 'python_main.py',
    }.get(lang, None)
    if not handler:
        raise NotSupportedLanguage('Plugin language not supported.')
    process = {
        # 'cpp': Popen([os.path.join(path, handler)], stdin=PIPE, stdout=PIPE, stderr=None),
        'py': Popen([sys.executable, os.path.join(path, handler), name], stdin=PIPE, stdout=PIPE, stderr=None, universal_newlines=True),
    }.get(lang, None)
    if not process:
        raise RuntimeError('Spawning a dedicated process for ' + name + ' failed.')
    return process
