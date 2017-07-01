from queue import Queue
from .utils import Singleton



class QueueCommand(Queue, metaclass=Singleton):
    pass


class QueuePlugin(Queue, metaclass=Singleton):
    pass


class QueueTtS(Queue, metaclass=Singleton):
    pass
