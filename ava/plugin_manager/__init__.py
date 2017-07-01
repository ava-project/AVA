from ..queues import QueuePluginManage, QueueTtS
from ..components import _BaseComponent
from .plugin_builtins import PluginBuiltins

class PluginManager(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_plugin_manage = QueuePluginManage()
        self.queue_tts = QueueTtS()


    def run(self):
        command = self.queue_plugin_manage.get()
        print('Plugin manager execute : {}'.format(command))
        target = command.split(' ')
        if len(target) > 1:
            try:
                result = getattr(PluginBuiltins, target[0])(str(' '.join(target[1:])))
                self.queue_tts.put(result)
            except Exception as err:
                self.queue_tts.put(str(err))
        else:
            self.queue_tts.put('Plugin builtin [' + target[0] + '] missing 1 argument.')
        self.queue_plugin_manage.task_done()
