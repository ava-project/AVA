from ..components import _BaseComponent
from .FileCrawler import FileCrawler

import os
import sys
import multiprocessing
import subprocess

class BuiltinRunner(_BaseComponent):

    def __init__(self, queues):
        super().__init__(queues)
        self.file_crawler = FileCrawler()
        self.queue_builtin = None
        self.queue_tts = None

    def setup(self):
        self.queue_builtin = self._queues['QueueBuiltinRunner']
        self.queue_tts = self._queues['QueueTextToSpeech']

    def run(self):
        while self._is_init:
            event = self.queue_builtin.get()
            if event is None:
                break
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
    
    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_builtin.put(None)
