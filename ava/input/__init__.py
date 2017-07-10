import sys
from ..queues import QueueInput
from ..components import _BaseComponent
from .RawInput import RawInput
from pynput import keyboard
import wave

class Input(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.input_queue = QueueInput()
        self.input_listener = RawInput()

    def writeToFile(self, all_datas):
        wf = wave.open("sample.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b''.join(all_datas))
        wf.close()

    def on_press(self,key):
        try:
            if key == key.f2:
                print("on_press..")
                self.input_listener.start()
                self.input_listener.reading_thread = threading.Thread(target=self.input_listener.read)
                self.input_listener.reading_thread.start()
                input()
        except AttributeError:
            pass


    def on_release(self,key):
        if key == key.enter:
            print("on_release..")
            self.input_listener.stop()
            while self.input_listener.done == False:
                pass
            self.writeToFile(self.input_listener.audio, self.input_listener.record)
            self.input_queue.put(True)
            return False

    def run(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
