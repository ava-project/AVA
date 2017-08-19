
class _ListenerInterface(object):

    def __init__(self, state, store, tts):
        self.state = state
        self.store = store
        self.queue_tts = tts

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
