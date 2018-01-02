import io
import sys
import threading
import wave

from pynput import keyboard
from pynput.keyboard import Key, Controller

from .RawInput import RawInput
from ..components import _BaseComponent

class KeyManager:
    def __init__(self, queues):
        self.activated = False
        self.listener = None
        self.input_listener = RawInput()
        self.activated = False
        self.input_queue = queues

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
            if key == Key.ctrl and not self.activated:
                self.activated = True
                print ("Voice recognition activated ! Release when you are done...")
                self.input_listener.reading_thread = threading.Thread(target=self.input_listener.read)
                self.input_listener.reading_thread.start()
        except AttributeError:
            print ("Error on Key pressed")
            pass

    def on_release(self, key):
        if self.activated:
            self.activated = False
            self.input_listener.stop()
            print ("Voice recognition stopped !")
            while self.input_listener.done == False:
                pass
            self.write_to_file(self.input_listener.record)

    def run(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as self.listener:
            self.listener.join()

    def stop(self):
        print('Stopping {0}...'.format(self.__class__.__name__))
        self.listener.stop()

    def running(self):
        print ("Press Ctrl to activate the Voice Recognition...")
