print('{}: name = {}'.format(__file__, __name__))

from .components import ComponentManager
from .input import Input
from .no_vocal_test import NoVocalTest
from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech
from .builtin_runner import BuiltinRunner
from .server import DaemonServer
from .mobile_bridge_input import MobileBridgeInput
from .dispatcher import Dispatcher
from .plugins import PluginManager, PluginInvoker, PluginListener

class AVA(object):
    def __init__(self):
        self.manager = ComponentManager()
        import avasdk
        if avasdk.__version__ != '1.0.5':
            import sys
            sys.exit('AVA requires the version (1.0.5) of the Software Development Kit.')

    def run(self):
        self.manager.add_component(Input)
        self.manager.add_component(Dispatcher)
        self.manager.add_component(NoVocalTest)
        self.manager.add_component(SpeechToText)
        self.manager.add_component(TextToSpeech)
        self.manager.add_component(DaemonServer)
        self.manager.add_component(MobileBridgeInput)
        self.manager.add_component(BuiltinRunner)
        self.manager.add_component(PluginManager)
        self.manager.add_component(PluginInvoker)
        self.manager.add_component(PluginListener)
        self.manager.start_all()
        from .state import State
        State().loading_done()
        self.manager.ready()
        self.manager.join_all()

    def stop(self):
        print('Exiting AVA')
        self.manager.stop_all()

def main():
    print('main(): start')
    ava = AVA()
    try:
        from .loading import loading
        loading(plugins_nbr=0, process_time=6, target='plugins')
        ava.run()
    except Exception as err:
        print(str(err))
    except KeyboardInterrupt as err:
        ava.stop()
        print('main(): stop')
    print('main(): end')