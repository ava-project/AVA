from ..queues import QueueBuiltin, QueueTtS
from ..components import _BaseComponent
from .FileCrawler import FileCrawler

import os
import sys
import multiprocessing
import subprocess

class BuiltinRunner(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_builtin = QueueBuiltin()
        self.queue_tts = QueueTtS()
        self.file_crawler = FileCrawler()

    def run(self):
        event = self.queue_builtin.get()
        command = ' '.join('{}'.format(value) for key, value in event.items() if value)
        command_list = command.rsplit()
        target = self.execute_order(command);
        if target is None :
            print('No file or application corresponding found : {}'.format(command))
        else :
            print('Builtin runner execute : {}'.format(command))
            if (os.name == 'nt') :
                p = multiprocessing.Process(target=os.startfile, args=(target,))
                p.daemon = True
                p.start()
            else:
                p = subprocess.Popen(target, shell=True)
        self.queue_tts.put('task completed')
        self.queue_builtin.task_done()

    def execute_order(self, command):
        command_list = command.rsplit(' ')
        order = command_list[0]
        if order == 'exit':
            os._exit(0)
        elif (len(command_list) > 1):
            if order == 'open' :
                return self.file_crawler.find(command_list[1], False)
            else :
                return self.file_crawler.find(command_list[1])

    def shutdown(self):
        print('Shutting down the BuiltinRunner')
