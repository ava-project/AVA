import sys
from os import path
from time import sleep
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
    def __init__(self):
        self.manager = ComponentManager()
        self.config = ConfigLoader(path.dirname(path.realpath(__file__)))

    def run(self):
        self.config.load('settings.json')
        self.manager.add_component(Input)
        self.manager.add_component(SpeechToText)
        self.manager.add_component(MobileBridgeInput)
        self.manager.add_component(NoVocalTest)
        self.manager.add_component(Dispatcher)
        self.manager.add_component(BuiltinRunner)
        self.manager.add_component(PluginManager)
        self.manager.add_component(PluginInvoker)
        self.manager.add_component(TextToSpeech)
        self.manager.add_component(DaemonServer)
        self.manager.start_all()
        self.manager.join_all()

    def stop(self):
        print('Exiting AVA')
        self.manager.shutdown()

def main():
    ava = AVA()
    try:
        ava.run()
    except (KeyboardInterrupt):
        sys.stderr.close()
        ava.stop()
        sleep(5)


if __name__ == "__main__":
    main()
