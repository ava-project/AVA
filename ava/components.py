from threading import Thread
from queue import Empty
from .queues import *

class _BaseComponent(Thread):

    def __init__(self):
        super().__init__()
        self._is_init = True

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

class ComponentManager(object):

    def __init__(self):
        self.threads = []
        self._manager_queue = ManagerQueue()
        self._config_keys = {}

    def add_component(self, Component):
        component = Component()
        component.daemon = True
        if getattr(component, 'setup', None):
            component.setup()
        self.threads.append(component)

    def start_all(self):
        for t in self.threads:
            t.start()

    def stop_all(self):
        for t in self.threads:
            t.stop()

    def join_all(self):
        while True:
            for t in self.threads:
                t.join(0.5)
            try:
                cmd = self._manager_queue.get(False)
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
