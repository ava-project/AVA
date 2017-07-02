from ..queues import QueueCommand
from ..components import _BaseComponent, RunOneTime

# Sub components imports :
#   -Input interface
from .RawInput import RawInput
#   -Speech To Text engine
from .STT_Engine import STT_Engine

# Decoder instance imports
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


class SpeechToText(_BaseComponent, RunOneTime):

    def __init__(self):
        super().__init__()
        self.queue_command = QueueCommand()
        self.stt = STT_Engine()

    def run(self):
        print("AVA is listening, call her before a command !")
        in_speech_bf = False
        listen_for_command = False
        decoder = Decoder(self.stt.config)
        input_type = RawInput()
        input_type.start()
        decoder.start_utt()
        while True:
            buff = input_type.read()
            if buff:
                decoder.process_raw(buff, False, False)
                if decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = decoder.get_in_speech()
                    if not in_speech_bf:
                        decoder.end_utt()
                        result = decoder.hyp().hypstr
                        if listen_for_command == True:
                            if result:
                                self.queue_command.put(result)
                                result = ""

                        if (result == 'ava') and (listen_for_command == False):
                            print("Yes ? (call Text To Speech)")
                            result = ""
                            listen_for_command = True

                        decoder.start_utt()
            else:
                break
        decoder.end_utt()
