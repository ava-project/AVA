import threading
from queue import Queue

from .audio_input import AudioInput
from .vocal_interpretor import VocalInterpretor
from .executor import Executor
from .plugin_manager import PluginManager
from .text_to_speech import TextToSpeech

def worker_audio():
    audio_input = AudioInput()
    audio_input.run()

def worker_interpretor():
    vocal_interpretor = VocalInterpretor()
    vocal_interpretor.run()

def worker_executor():
    executor = Executor()
    executor.run()

def worker_plugin_manager():
    executor = PluginManager()
    executor.run()

def worker_tts():
    tts = TextToSpeech()
    tts.run()

class AVA(object):

    def run(self):
        t_audio = threading.Thread(target=worker_audio)
        t_audio.start()
        t_interpretor = threading.Thread(target=worker_interpretor)
        t_interpretor.start()
        t_executor = threading.Thread(target=worker_executor)
        t_executor.start()
        t_plugin_manager = threading.Thread(target=worker_plugin_manager)
        t_plugin_manager.start()
        t_text_to_speech = threading.Thread(target=worker_tts)
        t_text_to_speech.start()
        ############
        t_audio.join()
        t_interpretor.join()
        t_executor.join()
        t_plugin_manager.join()
        t_text_to_speech.join()


def main():
    test = AVA()
    test.run()


if __name__ == "__main__":
    main()
