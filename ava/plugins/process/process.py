import os
import sys
import datetime
from subprocess import Popen, PIPE, STDOUT

class NotSupportedLanguage(Exception):
    pass

def multi_lines_output_handler(output):
    """
    """
    return '\n'.join(output) if len(output) > 1 else ''.join(output), True if len(output) > 1 else False

def clean_outpout_after_runtime_import(output):
    """
    """
    if '__END_OF_IMPORT__' in output:
        index = 0
        target = output.index('__END_OF_IMPORT__')
        while index <= target:
            output.remove(index)
            index += 1
    return output

def flush_process_output(process, tokens):
    """
    """
    output = []
    while True:
        line = process.stdout.readline().rstrip()
        if any(x in line for x in tokens):
            break
        output.append(line)
    return output

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
