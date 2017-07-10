from ..queues import QueueCommand, QueueInput
from ..components import _BaseComponent, RunOneTime

# Sub components imports :
#   -Input interface
# from .RawInput import RawInput
from pynput import keyboard
#   -Speech To Text engine
from .STT_Engine import STT_Engine


class SpeechToText(RunOneTime, _BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()
        self.queue_input = QueueInput()
        self.stt = STT_Engine()

    def run(self):
        audio_stream = self.queue_input.get()
        self.stt.recognize(audio_stream)
        # self.queue_command.put()#CONCATENATE RESULT)
