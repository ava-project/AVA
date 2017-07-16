from os import path
from .components import ComponentManager
from .input import Input
from .dispatcher import Dispatcher
from .builtin_runner import BuiltinRunner
from .plugins import PluginInvoker, PluginManager
from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech
from .config import ConfigLoader
from .server import DaemonServer
from .no_vocal_test import NoVocalTest
from .mobile_bridge_input import MobileBridgeInput


class AVA(object):

    def run(self):
        config = ConfigLoader(path.dirname(path.realpath(__file__)))
        config.load('settings.json')
        manager = ComponentManager()
        manager.add_component(Input)
        manager.add_component(SpeechToText)
        manager.add_component(MobileBridgeInput)
        manager.add_component(NoVocalTest)
        manager.add_component(Dispatcher)
        manager.add_component(BuiltinRunner)
        manager.add_component(PluginManager)
        manager.add_component(PluginInvoker)
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
