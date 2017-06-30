from queue import Queue
from .utils import Singleton


class QueueAudio(Queue, metaclass=Singleton):
    pass


class QueueCommand(Queue, metaclass=Singleton):
    pass


class QueuePlugin(Queue, metaclass=Singleton):
    pass


class QueueTtS(Queue, metaclass=Singleton):
    pass
