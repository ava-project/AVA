from queue import Queue


class _BaseQueue(Queue):

    def __new__(cls, *args, **kwargs):
        """
        Singleton Queue
        """
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
            print('Creating {}'.format(cls.__name__))
        return cls._inst


class QueueAudio(_BaseQueue):
    pass


class QueueCommand(_BaseQueue):
    pass


class QueuePluginCommand(_BaseQueue):
    pass


class QueueTtS(_BaseQueue):
    pass
