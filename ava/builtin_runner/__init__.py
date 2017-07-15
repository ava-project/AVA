from ..queues import QueueBuiltin, QueueTtS
from ..components import _BaseComponent
from .FileCrawler import FileCrawler

import os
import multiprocessing

class BuiltinRunner(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_builtin = QueueBuiltin()
        self.queue_tts = QueueTtS()
        self.file_crawler = FileCrawler()

    def run(self):
        command = self.queue_builtin.get()
        command_list = command.rsplit()
        target = self.execute_file(command);
        if target is None :
            print('No file or application corresponding found : {}'.format(command))
        else :
            print('Builtin runner execute : {}'.format(command))
            p = multiprocessing.Process(target=os.startfile, args=(target,))
            p.start()
            p.join()
        self.queue_tts.put('task completed')
        self.queue_builtin.task_done()

    def execute_file(self, command) :
        command_list = command.rsplit(' ')
        order = command_list[0]
        if order == 'help':
            return 'help'
        elif (len(command_list) > 1) :
            if order == 'open' :
                return self.file_crawler.find(command_list[1], False)
            else :
                return self.file_crawler.find(command_list[1])
