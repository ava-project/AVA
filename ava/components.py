from threading import Thread


class _BaseComponent(object):

    def run(self, *args, **kwargs):
        raise NotImplemented()


class ComponentManager(object):

    def __init__(self):
        self.threads = []

    def add_component(self, Component):
        t = Thread(target=self.worker, args=(Component,))
        t.daemon = True
        self.threads.append(t)

    def worker(self, Component):
        component = Component()
        component.run()

    def start_all(self):
        for t in self.threads:
            t.start()

    def join_all(self):
        for t in self.threads:
            t.join()
