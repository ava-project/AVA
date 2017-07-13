import os
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
    log = plugin.get_log_file()
    lang = plugin.get_specs()['lang']
    path = os.path.join('ava', 'plugins', 'process')
    handler = {
        'cpp': 'cpp_plugin_process.py',
        'go': 'golang_plugin_process.py',
        'py': 'python_plugin_process.py',
    }.get(lang, None)
    if not handler:
        raise NotSupportedLanguage('Error: Plugin language not supported.')
    log.write(datetime.datetime.now().strftime('### %Y-%m-%d %H:%M:%S ###\n')) and log.flush()
    # TODO fix binary name depending on the os
    process = Popen(['python3', os.path.join(path, handler), name], stdin=PIPE, stdout=PIPE, stderr=log, universal_newlines=True)
    return process
