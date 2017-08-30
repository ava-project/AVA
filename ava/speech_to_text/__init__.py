from ..components import _BaseComponent

# Sub components imports :
#   -Speech To Text engine
from .STT_EngineWebsocket import STT_Engine_WebSocket as STT_Engine


class SpeechToText(_BaseComponent):

    def __init__(self, queues):
        super().__init__(queues)
        self.queue_command = None
        self.queue_input = None
        self.queue_tts = None
        self.stt = STT_Engine()

    def setup(self):
        self.queue_command = self._queues['QueueDispatcher']
        self.queue_input = self._queues['QueueInput']
        self.queue_tts = self._queues['QueueTextToSpeech']

    def run(self):
        while self._is_init:
            audio_stream = self.queue_input.get()
            if audio_stream is None:
                break
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

    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_input.put(None)
