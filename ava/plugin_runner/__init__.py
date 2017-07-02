from ..queues import QueuePluginCommand, QueueTtS
from ..components import _BaseComponent
from ..plugin_store import PluginStore

class PluginRunner(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.store = PluginStore()
        self.queue_plugin_command = QueuePluginCommand()
        self.queue_tts = QueueTtS()

    def run(self):
        command = self.queue_plugin_command.get()
        print('Plugin runner execute : {}'.format(command))
        # TODO check if the plugin is installed
        # TODO execute the command
        self.queue_tts.put('task completed')
        self.queue_plugin_command.task_done()
