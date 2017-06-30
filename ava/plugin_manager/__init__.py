

class PluginManager(object):

    def __init__(self, queue_plugin, queue_tts):
        super().__init__()
        self.queue_plugin = queue_plugin
        self.queue_tts = queue_tts

    def run(self):
        while True:
            command = self.queue_plugin.get()
            print('Plugin manager execute : {}'.format(command))
            self.queue_tts.put('task completed')
            self.queue_plugin.task_done()
