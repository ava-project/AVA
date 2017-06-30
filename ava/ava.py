import threading
from queue import Queue

from .audio_input import AudioInput
from .vocal_interpretor import VocalInterpretor
from .executor import Executor
from .plugin_manager import PluginManager
from .text_to_speech import TextToSpeech

def worker_audio(queue_audio):
    audio_input = AudioInput(queue_audio)
    audio_input.run()

def worker_interpretor(queue_audio, queue_command):
    vocal_interpretor = VocalInterpretor(queue_audio, queue_command)
    vocal_interpretor.run()

def worker_executor(queue_command, queue_plugin):
    executor = Executor(queue_command, queue_plugin)
    executor.run()

def worker_plugin_manager(queue_plugin, queue_tts):
    executor = PluginManager(queue_plugin, queue_tts)
    executor.run()

def worker_tts(queue_tts):
    tts = TextToSpeech(queue_tts)
    tts.run()

class AVA(object):

    def __init__(self):
        self.queue_audio = Queue()
        self.queue_command = Queue()
        self.queue_plugin = Queue()
        self.queue_tts = Queue()

    def run(self):
        t_audio = threading.Thread(target=worker_audio, args=(self.queue_audio,))
        t_audio.start()
        t_interpretor = threading.Thread(target=worker_interpretor,
            args=(self.queue_audio, self.queue_command))
        t_interpretor.start()
        t_executor = threading.Thread(target=worker_executor,
            args=(self.queue_command, self.queue_plugin))
        t_executor.start()
        t_plugin_manager = threading.Thread(target=worker_plugin_manager,
            args=(self.queue_plugin, self.queue_tts))
        t_plugin_manager.start()
        t_text_to_speech = threading.Thread(target=worker_tts,
            args=(self.queue_tts,))
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
