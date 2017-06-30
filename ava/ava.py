from .components import ComponentManager

from .audio_input import AudioInput
from .vocal_interpretor import VocalInterpretor
from .executor import Executor
from .plugin_manager import PluginManager
from .text_to_speech import TextToSpeech

class AVA(object):

    def run(self):
        manager = ComponentManager()
        manager.add_component(AudioInput)
        manager.add_component(VocalInterpretor)
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
    except KeyboardInterrupt:
        test.stop()


if __name__ == "__main__":
    main()
