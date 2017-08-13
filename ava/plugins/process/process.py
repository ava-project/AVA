import os
import sys
import datetime
from subprocess import Popen, PIPE, STDOUT
from avasdk.plugins.log import IMPORT, DELIMITER


class NotSupportedLanguage(Exception):
    """Source code of a plugin is written in language which is currently not supported by AVA.
    """
    pass


def multi_lines_output_handler(output):
    """Output handler.

        @param:
            - output: An array containing all lines of an output performed by a plugin (array).

        @return:
            - Tuple:
                * A new well formed array containing the output (array).
                * A boolean to determine if there are many lines (boolean).
    """
    return '\n'.join(output) if len(output) > 1 else ''.join(output), True if len(output) > 1 else False

def flush_stdout(process):
    """Flush the data written of the stdout of the given process.

        @param:
            - process: The process object (subprocess.Popen).

        @return:
            - the output flushed (array).
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
    """Spawn a new process dedicated to the plugin 'plugin'.

        @param:
            - plugin: The name of the plugin for which a new process is required (string).

        @return:
            - The new process (subprocess.Popen), None if fail.
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
