from ...process import flush_stdout
from .interface import _ListenerInterface
from ...process import multi_lines_output_handler
from avasdk.plugins.log import ERROR, IMPORT, REQUEST, RESPONSE

class _WindowsInterface(_ListenerInterface):
    """
    """

    def __init__(self, state, store, tts):
        """
        """
        super().__init__(state, store, tts)

    def listen(self):
        """
        """
        # TODO find a way to handle it on Windows
        print('Run _WindowsInterface')

    def stop(self):
        """
        """
        print('Stop _WindowsInterface')
