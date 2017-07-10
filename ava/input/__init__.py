import io
import sys
import threading
import wave

from pynput import keyboard

from .RawInput import RawInput
from ..queues import QueueInput
from ..components import _BaseComponent


class Input(_BaseComponent):

    def __init__(self):
        super().__init__()
        self.input_queue = QueueInput()
        self.input_listener = RawInput()

    def write_to_file(self, all_datas):
        audio_file = io.BytesIO()
        wf = wave.Wave_write(audio_file)
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b''.join(all_datas))
        audio_file.seek(0)
        self.input_queue.put(audio_file)

    def on_press(self, key):
        try:
            if key == key.cmd:
                print("on_press..")
                self.input_listener.start()
                self.input_listener.reading_thread = threading.Thread(target=self.input_listener.read)
                self.input_listener.reading_thread.start()
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(self, key):
        if key == key.cmd:
            print('on_release')
            self.input_listener.stop()
            while self.input_listener.done == False:
                pass
            self.write_to_file(self.input_listener.record)
            return False


    def run(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
