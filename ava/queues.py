from queue import Queue
from .utils import Singleton


class QueueCommand(Queue, metaclass=Singleton):
    pass


class QueuePluginCommand(Queue, metaclass=Singleton):
    pass


class QueuePluginManage(Queue, metaclass=Singleton):
    pass


class QueueBuiltin(Queue, metaclass=Singleton):
    pass


class QueueTtS(Queue, metaclass=Singleton):
    pass
