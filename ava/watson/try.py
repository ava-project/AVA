#from ws4py.client.threadedclient import WebSocketClient
#import base64, json, ssl, subprocess, threading, time, pyaudio

from stt_watson.SttWatson import SttWatson
from stt_watson.SttWatsonAbstractListener import SttWatsonAbstractListener

class MyListener(SttWatsonAbstractListener):
    def __init__(self):
        pass
    """
    This give hypothesis from watson when your sentence is finished
    """
    def listenHypothesis(self, hypothesis):
        print ("Hypothesis: {0}".format(hypothesis))

    """
    This give the json received from watson
    """
    def listenPayload(self, payload):
        print(u"Text message received: {0}".format(payload))
    """
    This give hypothesis from watson when your sentence is not finished
    """
    def listenInterimHypothesis(self, interimHypothesis):
        print ("Interim hypothesis: {0}".format(interimHypothesis))


myListener = MyListener()
sttWatson = SttWatson('b189f5ce-1f20-4dd9-a97d-0b49b9bd2318', 'cUHVuqPzAOvP')
sttWatson.addListener(myListener)
sttWatson.run()
