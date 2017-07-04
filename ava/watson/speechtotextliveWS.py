
##Install Websocket pip install ws4py
from ws4py.client.threadedclient import WebSocketClient
import base64, json, ssl, subprocess, threading, time, pyaudio

class SpeechToTextClient(WebSocketClient):
    def __init__(self):
        ## CREDENTIALS
        ## As their server is under Linux we have to give the credentials encoded and Linux friendly
        ws_url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
        username='b189f5ce-1f20-4dd9-a97d-0b49b9bd2318'
        password='cUHVuqPzAOvP'
        #        auth_string = "%s:%s" % (username, password)
        #base64string = base64.b64encode(auth_string)
        base64string = "YjE4OWY1Y2UtMWYyMC00ZGQ5LWE5N2QtMGI0OWI5YmQyMzE4OmNVSFZ1cVB6QU92UA=="
        base64string = base64string.replace('\n', '')

        self.listening = False

        try:
            ## WEBSOCKET
            ## Opening Webocket
            WebSocketClient.__init__(self, ws_url,
                                     headers=[("Authorization", "Basic %s" % base64string)])
            self.connect()
        except:
            print ("Failed to open WebSocket.")

    def opened(self):
        ##OPEN
        ##Setting configuration tools for the audio streaming

        print ('open.....')
        self.send('{"action": "start", "content-type": "audio/l16;rate=16000"}')
        self.stream_audio_thread = threading.Thread(target=self.stream_audio)
        self.stream_audio_thread.start()

    def received_message(self, message):
        ##Answer success from server
        print ('message receiving..')
        message = json.loads(str(message))
        if "state" in message:
            if message["state"] == "listening":
                self.listening = True
        print ("Message: " + str(message))

    def stream_audio(self):
        ## LISTENING
        ## Listening part part of the program
        print ('stream_audio...')
        while not self.listening:
            time.sleep(0.1)

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=2048)

        while self.listening:
            data = stream.read(1024)
            try:
                self.send(bytearray(data), binary=True)
            except ssl.SSLError:
                print ("fail")
                pass

    def close(self):
        ##CLOSE
        ##Closing all instances
        self.listening = False
        self.stream_audio_thread.join()
        WebSocketClient.close(self)


def main():
    try:
        stt_client = SpeechToTextClient()
        input()
    finally:
        stt_client.close()

if __name__ == "__main__":
    main()
