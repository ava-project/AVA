from threading import Thread


class _BaseComponent(object):

    def run(self, *args, **kwargs):
        raise NotImplemented()


class ComponentManager(object):

    def __init__(self):
        self.threads = []

    def add_component(self, Component):
        t = Thread(target=self._worker, args=(Component,))
        t.daemon = True
        self.threads.append(t)

    def _worker(self, Component):
        component = Component()
        need_loop = getattr(component, 'loop_on_run', True)
        component.run()
        while need_loop:
            component.run()
        print('Component {} exit'.format(Component.__name__))

    def start_all(self):
        for t in self.threads:
            t.start()

    def join_all(self):
        for t in self.threads:
            t.join()
