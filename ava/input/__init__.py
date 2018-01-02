import io
import sys
import threading
import wave

from ..components import _BaseComponent
from ..config import ConfigLoader
from .KeyManager import KeyManager
from .MobileInput import MobileInput

class Input(_BaseComponent):

    def __init__(self, queues):
        super().__init__(queues)
        self.input_queue = None
        self.active = True
        self.currentInput = 'raw'
        self.config = ConfigLoader(None, None)
        self.config.subscribe('InputConfig', 'STT')
        self.currentClassInput = None

    def setup(self):
        self.input_queue = self._queues['QueueInput']

    def run(self):
        self.currentClassInput = KeyManager(self.input_queue)
        self.currentClassInput.run()
        while self.active:
            newConfig = self.config.get('InputConfig')
            if newConfig is not None:
                self.switchConfig(newConfig)

    def switchConfig(newConfig):
        if self.currentClassInput is not None:
            self.currentClassInput.stop()
        if newConfig == "STT raw":
            self.currentClassInput = KeyManager(self.input_queue)
        elif newConfig == "STT mobile":
            self.currentClassInput = MobileInput(self.input_queue)
        self.currentClassInput.run()

    def stop(self):
        self.active = False
