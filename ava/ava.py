from os import path
from .components import ComponentManager
from .dispatcher import Dispatcher
from .builtin_runner import BuiltinRunner
# from .speech_to_text import SpeechToText
from .plugin_manager import PluginManager
from .plugin_runner import PluginRunner
from .text_to_speech import TextToSpeech
from .input import Input
from .config import ConfigLoader
from .server import DaemonServer

class AVA(object):

    def run(self):
        config = ConfigLoader(path.dirname(path.realpath(__file__)))
        config.load('settings.json')
        manager = ComponentManager()
        manager.add_component(Input)
        manager.add_component(Dispatcher)
        manager.add_component(BuiltinRunner)
        # manager.add_component(SpeechToText)
        manager.add_component(PluginManager)
        manager.add_component(PluginRunner)
        manager.add_component(TextToSpeech)
        manager.add_component(DaemonServer)
        manager.start_all()
        manager.join_all()

    def stop(self):
        print('Exiting AVA')

def main():
    test = AVA()
    try:
        test.run()
    except (KeyboardInterrupt):
        test.stop()


if __name__ == "__main__":
    main()
