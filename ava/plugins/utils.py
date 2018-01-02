import subprocess
# SDK
from avasdk.plugins.log import Logger
# local imports
from ..state import State
from ..utils import Singleton

__all__ = ['State', 'Singleton']


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


def flush_stdout(process: subprocess.Popen) -> tuple:
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
        if process is not None and isinstance(
                process, subprocess.Popen) and not process.stdout.closed:
            line = process.stdout.readline().rstrip()
            if line == Logger.DELIMITER:
                break
            output.append(line)
    return output, True if Logger.IMPORT in output else False
