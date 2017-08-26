import platform
from os import path
from threading import Thread
from queue import Queue, Empty
from .config import ConfigLoader

class _BaseComponent(Thread):

    def __init__(self, queues):
        super().__init__()
        self._is_init = True
        self._queues = queues

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

class ComponentManager(object):

    def __init__(self):
        self._components = []
        self._config_keys = {}
        self._queues = {}
        self._queues['QueueWindowsListener'] = Queue()
        self._queues['QueueComponentManager'] = Queue()
        self._config = ConfigLoader(path.dirname(path.realpath(__file__)), self._queues)
        self._config.load('settings.json')
        # if platform.system() == 'Windows':
        #     self._queues['QueueWindowsListener'] = Queue()


    def add_component(self, Component):
        component = Component(self._queues)
        component.daemon = True
        self._components.append(component)
        self._queues['Queue{0}'.format(Component.__name__)] = Queue()
        self._queues['ConfigQueue{0}'.format(Component.__name__)] = Queue()

    def start_all(self):
        for component in self._components:
            if getattr(component, 'setup', None):
                component.setup()
            component.start()

    def stop_all(self):
        print(self._components)
        for component in self._components:
            print('[{0}]'.format(component.__class__.__name__))
            component.stop()

    def join_all(self):
        while True:
            for component in self._components:
                component.join(0.1)
            try:
                cmd = self._queues['QueueComponentManager'].get(False)
            except Empty:
                pass
            else:
                func, *args = cmd.split(' ')
                getattr(self, func)(*args)

    def subscribe(self, component_name, key):
        print('subscribe')
        list_component = self._config_keys.get(key)
        if list_component is None:
            list_component = [component_name]
        else:
            list_component.append(component_name)
        self._config_keys[key] = list_component

    def update(self, key, value):
        print('update')
        list_component = self._config_keys.get(key)
        for component in list_component:
            self._queues['ConfigQueue{0}'.format(component)].put('{0} {1}'.format(key, value))
