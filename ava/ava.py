from .components import ComponentManager

from .speech_to_text import SpeechToText
from .executor import Executor
from .plugin_manager import PluginManager
from .text_to_speech import TextToSpeech

class AVA(object):

    def run(self):
        manager = ComponentManager()
        manager.add_component(SpeechToText)
        manager.add_component(Executor)
        manager.add_component(PluginManager)
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
