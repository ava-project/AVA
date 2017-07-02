from .components import ComponentManager
from .audio_input import AudioInput
from .dispatcher import Dispatcher
from .builtin_runner import BuiltinRunner
from .speech_to_text import SpeechToText
from .plugin_manager import PluginManager
from .plugin_runner import PluginRunner
from .text_to_speech import TextToSpeech

class AVA(object):

    def run(self):
        manager = ComponentManager()
        manager.add_component(AudioInput)
        manager.add_component(Dispatcher)
        manager.add_component(BuiltinRunner)
        manager.add_component(SpeechToText)
        manager.add_component(PluginManager)
        manager.add_component(PluginRunner)
        manager.add_component(TextToSpeech)
        manager.start_all()
        manager.join_all()

    def stop(self):
        print('Exiting AVA')

def main():
    test = AVA()
    try:
        test.run()
    except (KeyboardInterrupt, EOFError):
        test.stop()


if __name__ == "__main__":
    main()
