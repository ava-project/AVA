import os
import sys
import datetime
from subprocess import Popen, PIPE, STDOUT
from avasdk.plugins.log import IMPORT, DELIMITER


class NotSupportedLanguage(Exception):
    """Exception type NotSupportedLanguage. Raised when AVA detects that the Source
    code of a plugin is written in a non supported language.
    """
    pass


def multi_lines_output_handler(output):
    """Output handler to determine if it contains several lines.

    param:
        - output: An array containing all lines of an output performed by a plugin (array).
    return:
        - Tuple:
            * A new well formed array containing the output (array).
            * A boolean to determine if there were several lines (boolean).
    """
    return '\n'.join(output) if len(output) > 1 else ''.join(output), True if len(output) > 1 else False

def flush_stdout(process):
    """Flush the data written on the stdout of the given process.

    param:
        - process: The process object (subprocess.Popen).
    return:
        - the output flushed (array).
    """
    assert process is not None
    output = []
    while True:
        try:
            line = process.stdout.readline().rstrip()
        except:
            raise
        if line == DELIMITER:
            break
        output.append(line)
    return output, True if IMPORT in output else False

def spawn(plugin):
    """Spawn a new dedicated process for the plugin named 'plugin'.

    param:
        - plugin: The name of the plugin for which a new process is required (string).
    return:
        - The new process (subprocess.Popen), None if it fails.
    """
    name = plugin.get_name()
    lang = plugin.get_specs()['lang']
    path = os.path.join('ava', 'plugins', 'process')
    handler = {
        'py': 'python_main.py',
    }.get(lang, None)
    if not handler:
        raise NotSupportedLanguage('Plugin language not supported.')
    return Popen([sys.executable, os.path.join(path, handler), name], stdin=PIPE, stdout=PIPE, stderr=None, universal_newlines=True)
