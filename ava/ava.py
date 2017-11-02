from .state import State
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
        State().loading_done()
        self.manager.ready()
        self.manager.join_all()

    def stop(self):
        print('Exiting AVA')
        self.manager.stop_all()

def loading():
    """
    """
    import os
    import sys
    from time import sleep
    sleep(0.25)
    plugins_nbr = 0
    path = os.path.join(os.path.expanduser('~'), '.ava', 'plugins')
    for element in os.listdir(path):
        if os.path.isdir(os.path.join(path, element)):
            plugins_nbr += 1
    n = plugins_nbr * 6
    for i in range(n):
        sys.stdout.write('\r')
        j = (i + 1) / n
        if not State().is_loading() or j > 1:
            break
        sys.stdout.write("Loading plugins [%-20s] %d%%" % ('='*int(20*j), 100*j))
        sys.stdout.flush()
        sleep(n / 100 * (plugins_nbr / 3))

def main():
    ava = AVA()
    try:
        import threading
        threading.Thread(target=ava.run).start()
        threading.Thread(target=loading).start()
    except Exception as err:
        print(str(err))
    except KeyboardInterrupt as err:
        ava.stop()

if __name__ == "__main__":
    main()
