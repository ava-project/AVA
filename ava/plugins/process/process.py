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

def flush_stdout(process):
    """
    """
    assert process is not None
    output = []
    while True:
        line = process.stdout.readline().rstrip()
        if line == DELIMITER:
            break
        output.append(line)
    return output, True if IMPORT in output else False

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
        raise RuntimeError('Spawning a dedicated process for {} failed.'.format(name))
    return process
