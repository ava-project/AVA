from threading import Thread


class _BaseComponent(object):

    def run(self, *args, **kwargs):
        raise NotImplemented()


class ComponentManager(object):

    def __init__(self):
        self.threads = []

    def add_component(self, Component):
        component = Component()
        t = Thread(target=self.worker, args=(component,))
        self.threads.append(t)

    def worker(self, component):
        component.run()

    def start_all(self):
        for t in self.threads:
            t.start()

    def join_all(self):
        for t in self.threads:
            t.join()
