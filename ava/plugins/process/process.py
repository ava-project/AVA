import os
import sys
import datetime
from subprocess import Popen, PIPE, STDOUT
from avasdk.plugins.log import IMPORT, DELIMITER


class NotSupportedLanguage(Exception):
    pass

def multi_lines_output_handler(output):
    """
    """
    return '\n'.join(output) if len(output) > 1 else ''.join(output), True if len(output) > 1 else False

def flush_process_output(process):
    """
    """
    output = []
    # print(process.stdout.name)
    while True:
        line = process.stdout.readline().rstrip()
        # if any(x in line for x in [DELIMITER, IMPORT]):
        if line == DELIMITER:
            break
        output.append(line)
    return output, True if IMPORT in output else False

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

def spawn(plugin):
    """
    """
    name = plugin.get_name()
    lang = plugin.get_specs()['lang']
    path = os.path.join('ava', 'plugins', 'process')
    handler = {
        'py': 'python_main.py',
    }.get(lang, None)
    if not handler:
        raise NotSupportedLanguage('Plugin language not supported.')
    process = {
        'py': Popen([sys.executable, os.path.join(path, handler), name], stdin=PIPE, stdout=PIPE, stderr=None, universal_newlines=True),
    }.get(lang, None)
    if not process:
        raise RuntimeError('Spawning a dedicated process for ' + name + ' failed.')
    return process
