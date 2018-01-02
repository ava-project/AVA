import queue
import subprocess
import select as sct
# local imports
from .interface import _ListenerInterface
from ...utils import State
from ...plugin import Plugin
from ...store import PluginStore


class _UnixInterface(_ListenerInterface):
    """
    The Unix interface responsible of listening each plugin's process
    running.
    """

    def __init__(self, state: State, store: PluginStore, tts: queue.Queue):
        """
        We initialize here the _UnixInterface by initializing the
        _ListenerInterface with the instances of the State, the PluginStore, the
        queue dedicated to the text-to-speech  component.

        :param state: The instance of the State object.
        :param store: The instance of the PluginStore.
        :param tts: The instance of the queue dedicated to the text-to-speech
         component
        """
        super().__init__(state, store, tts)

    def listen(self):
        """
        Main function of the _UnixInterface.

        Performs a poll on each stdout file descriptor of each process of each
        plugin installed. As soon as a read event is detected on the file
        descriptor of a process, that means a plugin has been run.
        The data are read and sent to the 'self._process_result' method
        inherited from the _ListenerInterface.
        """
        OBSERVED = {}
        POLL = sct.poll()
        READ_ONLY = sct.POLLIN | sct.POLLPRI | sct.POLLHUP | sct.POLLERR
        for _, plugin in self._store.get_plugins().items():
            process = plugin.get_process()
            if process is not None and isinstance(
                process, subprocess.Popen) and not process.stdout.closed:
                fd = int(process.stdout.name)
                OBSERVED[fd] = process
                POLL.register(fd, READ_ONLY)
        result = POLL.poll(0)
        for fd, _ in result:
            if OBSERVED.get(fd) is None:
                continue
            p = OBSERVED.get(fd)
            self._process_result(''.join(
                '{}'.format(k) for k, v in self._store.get_plugins().items()
                if p == v.get_process()), p)
