from ..queues import QueueCommand, QueueInput
from ..components import _BaseComponent, RunOneTime

# Sub components imports :
#   -Input interface
# from .RawInput import RawInput
from pynput import keyboard
#   -Speech To Text engine
from .STT_Engine import STT_Engine

import threading

class SpeechToText(RunOneTime, _BaseComponent, QueueInput):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()
        self.stt = STT_Engine()

    def run(self):
        if
        self.stt.sendFile()
        self.queue_command.put(#CONCATENATE RESULT)
