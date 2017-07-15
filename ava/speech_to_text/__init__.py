from ..queues import QueueCommand, QueueInput, QueueTtS
from ..components import _BaseComponent

# Sub components imports :
#   -Speech To Text engine
from .STT_Engine import STT_Engine


class SpeechToText(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()
        self.queue_input = QueueInput()
        self.queue_tts = QueueTtS()
        self.stt = STT_Engine()

    def run(self):
        audio_stream = self.queue_input.get()
        self.queue_tts.put("Wait ...")
        print ("Sending information to be translated...")
        try:
            result = self.stt.recognize(audio_stream)
            print ("Message received...")
            if result["results"][0]["alternatives"][0]["transcript"] :
                self.queue_command.put(result["results"][0]["alternatives"][0]["transcript"])
                self.queue_input.task_done()
                self.queue_tts.put("Okay")
        except:
            self.queue_tts.put("Retry your command please")
