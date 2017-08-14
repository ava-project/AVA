from threading import Thread, Event


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
        self.event = Event()

    def shutdown(self):
        self.event.set()

    def add_component(self, Component):
        t = Thread(target=self._worker, args=(Component, self.event))
        t.daemon = True
        self.threads.append(t)

    def _worker(self, Component, event):
        component = Component()
        if getattr(component, 'setup', None):
            component.setup()
        if getattr(component, 'loop_on_run', True):
            while not event.is_set():
                component.run()
            print('AVANT Shutdown')
            component.shutdown()
        else:
            component.run()
        print('Component {} exit'.format(Component.__name__))

    def start_all(self):
        for t in self.threads:
            t.start()

    def join_all(self):
        for t in self.threads:
            t.join()
