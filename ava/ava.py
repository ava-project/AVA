from .components import ComponentManager
from .input import Input
from .dispatcher import Dispatcher
from .builtin_runner import BuiltinRunner
# from .speech_to_text import SpeechToText
from .plugins import PluginInvoker, PluginManager
from .text_to_speech import TextToSpeech


class AVA(object):

    def run(self):
        manager = ComponentManager()
        manager.add_component(Input)
        manager.add_component(Dispatcher)
        manager.add_component(BuiltinRunner)
        # manager.add_component(SpeechToText)
        manager.add_component(PluginManager)
        manager.add_component(PluginInvoker)
        manager.add_component(TextToSpeech)
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
