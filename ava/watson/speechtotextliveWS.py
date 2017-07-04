##Install Websocket pip install ws4py, pyaudio

from ws4py.client.threadedclient import WebSocketClient
#import websocket
import base64, json, ssl, subprocess, threading, time, pyaudio, wave

class SpeechToTextClient(WebSocketClient):
    def __init__(self):
        ## CREDENTIALS
        ## As their server is under Linux we have to give the credentials encoded and Linux friendly
        ws_url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=en-US_BroadbandModel"
        username='9d526cf4-63de-47da-be7d-e5662d3cd1a9'
        password='oWaCHHSTzjkO'
        #        auth_string = "%s:%s" % (username, password)
        #base64string = base64.b64encode(auth_string)
        base64string = "OWQ1MjZjZjQtNjNkZS00N2RhLWJlN2QtZTU2NjJkM2NkMWE5Om9XYUNISFNUemprTw=="
        base64string = base64string.replace('\n', '')
        header_str = 'Authorization:Basic %s' % base64string
        print (header_str)

        self.listening = False

        try:
            ## WEBSOCKET
            ## Opening Webocket
            WebSocketClient.__init__(self, ws_url,
                                     headers=[("Authorization", "Basic %s" % base64string)])
            self.connect()
            #            websocket.enableTrace(True)
            #            self.ws = websocket.WebSocketApp("wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=en-US_BroadbandModel",
            #                                  on_message = self.received_message,
            #                                 on_open  = self.opened,
            #                                 header = [header_str])
            #            websockets.client.connect(ws_url, extra_headers=[("Authorization", "Basic %s" % base64string)])
            #            self.ws.connect()
            print("connected...")
        except:
            print ("Failed to open WebSocket.")

    def opened(self):
        ##OPEN
        ##Setting configuration tools for the audio streaming

        print ('open..... <----------')
        self.send('{"action" : "start", "content-type" : "audio/l16;rate=16000;channels=1"}')
        self.stream_audio_thread = threading.Thread(target=self.stream_audio)
        self.stream_audio_thread.start()
        print ('open..... ---------->')

    def received_message(self, message):
        ##Answer success from server
        print ('message receiving.. <------')
        message = json.loads(str(message))
        if "state" in message:
            if message["state"] == "listening":
                self.listening = True
        print ("Message: " + str(message))
        print ('Message receive out ------>')

    def stream_audio(self):
        ## LISTENING
        ## Listening part part of the program
        print ('stream_audio... <-------')
        while not self.listening:
            time.sleep(0.1)
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=2048)

        all_datas = []
        while self.listening:
            data = stream.read(2048)
            try:
                self.send(bytearray(data), binary=True)
                all_datas.append(data)
            except ssl.SSLError:
                print ("fail")
                pass
        wf = wave.open("sample.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(all_datas))
        wf.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        print ('stream_audio... ----------->')

    def close(self):
        ##CLOSE
        ##Closing all instances
        print('closing....')
        self.listening = False
        self.stream_audio_thread.join()
        self.WebSocketClient.close()


def main():
    try:
        stt_client = SpeechToTextClient()
        input("press enter to finish..")
    finally:
        stt_client.close()

if __name__ == "__main__":
    main()
