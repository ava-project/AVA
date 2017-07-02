from threading import Thread


class _BaseComponent(object):

    def run(self, *args, **kwargs):
        raise NotImplemented()


class RunOneTime(object):
    """
    Make the class run one time
    """

    def __init__(self, *args, **kwargs):
        self.loop_on_run = False
        super().__init__(*args, **kwargs)


class ComponentManager(object):

    def __init__(self):
        self.threads = []

    def add_component(self, Component):
        t = Thread(target=self._worker, args=(Component,))
        t.daemon = True
        self.threads.append(t)

    def _worker(self, Component):
        component = Component()
        if getattr(component, 'setup', None):
            component.setup()
        if getattr(component, 'loop_on_run', True):
            while True:
                component.run()
        else:
            component.run()
        print('Component {} exit'.format(Component.__name__))

    def start_all(self):
        for t in self.threads:
            t.start()

    def join_all(self):
        for t in self.threads:
            t.join()
