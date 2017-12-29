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
#
# AVA SDK version required
#
SDK_VERSION_REQUIRED = '1.0.5'
#
# Try to import the sdk.
#
try:
    from avasdk import __version__ as current_sdk_version
except ImportError:
    import sys
    print('no sdk found')
    sys.exit(1)


class AVA(object):
    def __init__(self):
        self.manager = ComponentManager()
        if current_sdk_version != SDK_VERSION_REQUIRED:
            import sys
            sys.exit(
                'AVA requires the version ({}) of the Software Development Kit.'.
                format(SDK_VERSION_REQUIRED))

    def run(self):
        self.manager.add_component(Input)
        self.manager.add_component(Dispatcher)
        self.manager.add_component(NoVocalTest)
        self.manager.add_component(SpeechToText)
        self.manager.add_component(TextToSpeech)
        # self.manager.add_component(DaemonServer)
        self.manager.add_component(MobileBridgeInput)
        self.manager.add_component(BuiltinRunner)
        self.manager.add_component(PluginManager)
        self.manager.add_component(PluginInvoker)
        self.manager.add_component(PluginListener)
        self.manager.start_all()
        self.manager.ready()
        self.manager.join_all()

    def stop(self):
        print('Exiting AVA')
        self.manager.stop_all()


def main():
    ava = AVA()
    try:
        ava.run()
    except Exception as err:
        print(str(err))
    except KeyboardInterrupt as err:
        ava.stop()
