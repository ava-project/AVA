from ..components import _BaseComponent
from ..config import ConfigLoader

import asyncio

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
        self.config = ConfigLoader(None, None)
        self.config.subscribe('SpeechToTextConfig', 'engine')

    def setup(self):
        self.queue_command = self._queues['QueueDispatcher']
        self.queue_input = self._queues['QueueInput']
        self.queue_tts = self._queues['QueueTextToSpeech']

    # Function calling STT_Engine Recognize with async call
    def run(self):
        while self._is_init:
            audio_stream = self.queue_input.get()
            STTConfig = self.config.get('SpeechToTextConfig')
            if STTConfig is not None:
                self.stt.switchServer(STTConfig)
            if audio_stream is None:
                break
            self.queue_tts.put("Wait ...")
            print ("Sending information to be translated...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.stt.recognize(audio_stream, self))

    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._is_init = False
        self.queue_input.put(None)
