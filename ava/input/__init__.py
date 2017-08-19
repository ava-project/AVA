import io
import sys
import threading
import wave

from pynput import keyboard

from .RawInput import RawInput
from ..components import _BaseComponent


class Input(_BaseComponent):

    def __init__(self, queues):
        super().__init__(queues)
        self.activated = False
        self.input_queue = None
        self.input_listener = RawInput()
        self.listener = None

    def setup(self):
        self.input_queue = self._queues['QueueInput']

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
            if key == key.shift and not self.activated:
                self.activated = True
                print ("Voice recognition activated ! Release when you are done...")
                self.input_listener.reading_thread = threading.Thread(target=self.input_listener.read)
                self.input_listener.reading_thread.start()
        except AttributeError:
            pass

    def on_release(self, key):
        if self.activated:
            self.activated = False
            self.input_listener.stop()
            print ("Voice recognition stopped !")
            while self.input_listener.done == False:
                pass
            self.write_to_file(self.input_listener.record)
            return False


    def run(self):
        print ("Press WINDOWS for PC or COMMAND for Mac to activate the Voice Recognition...")
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as self.listener:
            self.listener.join()

    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))
        self.listener.stop()
