import select
from .interface import _ListenerInterface

class _UnixInterface(_ListenerInterface):
    """
    """

    def __init__(self, state, store, tts, listener):
        """
        """
        super().__init__(state, store, tts, listener)

    def listen(self):
        """
        """
        OBSERVED = {}
        POLL = select.poll()
        READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
        for _, plugin in self.store.plugins.items():
            fd = int(plugin.get_process().stdout.name)
            OBSERVED[fd] = plugin.get_process()
            POLL.register(fd, READ_ONLY)
        result = POLL.poll(0)
        for fd, _ in result:
            if OBSERVED.get(fd) is None:
                continue
            p = OBSERVED.get(fd)
            self._process_result(''.join('{}'.format(k) for k, v in self.store.plugins.items() if p == v.get_process()), p)
