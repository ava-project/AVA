import os
import sys
import datetime
from subprocess import Popen, PIPE, STDOUT
from avasdk.plugins.log import Logger


class NotSupportedLanguage(Exception):
    """Exception type NotSupportedLanguage. Raised when AVA detects that the Source
    code of a plugin is written in a non supported language.
    """
    pass


def multi_lines_output_handler(output):
    """Output handler to determine if it contains several lines.

    Args:
        output: An array containing all lines of an output performed by a plugin (array).

    Returns:
        Tuple:
            * A new well formed array containing the output (array).
            * A boolean to determine if there were several lines (boolean).
    """
    return '\n'.join(output) if len(output) > 1 else ''.join(
        output), True if len(output) > 1 else False


def flush_stdout(process):
    """Flushes the data written on the stdout of the given process.

    Args:
        process: The process object (subprocess.Popen).

    Returns:
        the output flushed (array).
    """
    output = []
    while True:
        assert process is not None and not process.stdout.closed
        line = process.stdout.readline().rstrip()
        if line == Logger.DELIMITER:
            break
        output.append(line)
    return output, True if Logger.IMPORT in output else False

def spawn(plugin):
    """Spawn a new dedicated process for the plugin named 'plugin'.

    Args:
        plugin: The name of the plugin for which a new process is required (string).

    Returns:
        The new process (subprocess.Popen), None if it fails.
    """
    name = plugin.get_name()
    lang = plugin.get_specs()['lang']
    path = os.path.join('ava', 'plugins', 'process')
    if lang not in ['cpp', 'go', 'py']:
        raise NotSupportedLanguage('Plugin language not supported.')
    executable = os.path.join(
            os.path.expanduser('~'),
            '.ava',
            'plugins',
            name,
            'venv/bin/python3')
    virtualenv = Popen(
            [sys.executable, os.path.join(path, 'venv.py'), name],
            stdin=None,
            stdout=None,
            stderr=None)
    if not virtualenv:
        raise RuntimeError('Creating virtual environment for {}'.format(name))
    # import time
    # time.sleep(5)
    return Popen(
        [executable, os.path.join(path, 'main.py'), name, lang],
        stdin=PIPE,
        stdout=PIPE,
        stderr=None,
        universal_newlines=True)
