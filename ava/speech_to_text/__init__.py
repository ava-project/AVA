from ..queues import QueueCommand
from ..components import _BaseComponent, RunOneTime

# Sub components imports :
#   -Input interface
# from .RawInput import RawInput
from pynput import keyboard
#   -Speech To Text engine
from .STT_Engine import STT_Engine

import threading

class SpeechToText(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()
        self.stt = STT_Engine()

    def on_press(self,key):
        try:
            if key == key.f2:
                print("on_press..")
                self.stt.reading_thread = threading.Thread(target=self.stt.listen)
                self.stt.reading_thread.start()
                # maybe timeout to get the minimum stream size required (100 bytes)
                input()
        except AttributeError:
            pass


    def on_release(self,key):
        if key == key.enter:
            print("on_release..")
            # Stop listener
            self.stt.close()
            return False

    def run(self):
        print("AVA is listening, call her before a command !")
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
