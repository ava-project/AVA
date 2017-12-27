from sys import executable
from subprocess import Popen
from os.path import join, expanduser
from platform import system as current_os
from subprocess import Popen, PIPE, STDOUT, call as create_virtualenv
from avasdk.plugins.log import Logger


class NotSupportedLanguage(Exception):
    """
    Exception type NotSupportedLanguage. Raised when AVA detects that the Source
    code of a plugin is written in a non supported language.
    """
    pass


def multi_lines_output_handler(output: list) -> tuple:
    """
    Output handler to determine if it contains several lines.

    :param output: An array containing all lines of an output performed by a
     plugin (list).

    :return: Tuple:
            * A new well formed array containing the output (list).
            * A boolean to determine if there were several lines (boolean).
    """
    return '\n'.join(output) if len(output) > 1 else ''.join(
        output), True if len(output) > 1 else False


def flush_stdout(process: Popen) -> tuple:
    """
    Flushes the data written on the stdout of the given process.

    :param process: The process object (subprocess.Popen).

    :return: Tuple:
            - the output flushed (list).
            - a boolean to determine whether the output is due to an import or
             not
    """
    output = []
    while True:
        assert process is not None and not process.stdout.closed
        line = process.stdout.readline().rstrip()
        if line == Logger.DELIMITER:
            break
        output.append(line)
    return output, True if Logger.IMPORT in output else False


def spawn(plugin: str) -> Popen:
    """
    Spawn a new dedicated process for the plugin named 'plugin'.

    :param plugin: The name of the plugin for which a new process is
     required (string).

    :return: The new process (subprocess.Popen), None if it fails.
    """
    name = plugin.get_name()
    lang = plugin.get_specs()['lang']
    path = join('ava', 'plugins', 'process')
    if current_os() == 'Windows':
        venv_executable = 'venv/Scripts/python.exe'
    else:
        venv_executable = 'venv/bin/python3'
    py_venv = join(expanduser('~'), '.ava', 'plugins', name, venv_executable)
    if lang not in ['cpp', 'go', 'py']:
        raise NotSupportedLanguage('Plugin language not supported.')
    create_virtualenv([executable, join(path, 'venv.py'), name], stdout=None)
    return Popen(
        [py_venv, join(path, 'main.py'), name, lang],
        stdin=PIPE,
        stdout=PIPE,
        stderr=None,
        universal_newlines=True)
