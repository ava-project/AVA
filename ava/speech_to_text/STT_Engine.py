import json, pyaudio, wave, base64, threading
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1


class STT_Engine():

    def __init__(self):
        self.stt = SpeechToTextV1(
            username = '9d526cf4-63de-47da-be7d-e5662d3cd1a9',
            password = 'oWaCHHSTzjkO',
            x_watson_learning_opt_out=False
        )
        self.listening = True

    def listen(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=2048)

        all_datas = []
        print ("Recording.. Press enter to finish")
        while self.listening:
            data = stream.read(2048)
            all_datas.append(data)

        stream.stop_stream()
        stream.close()
        self.listening = True
        self.writeToFile(p, all_datas)
        p.terminate()

    def writeToFile(self, p, all_datas):
        wf = wave.open("sample.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(all_datas))
        wf.close()
        self.sendFile()

    def sendFile(self):
        with open('sample.wav', 'rb') as audio_file:
            print(json.dumps(self.stt.recognize(
                audio_file, content_type='audio/wav', timestamps=True,
                word_confidence=True),
                             indent=2))


    def close(self):
        self.listening = False

# def main():
#     try:
#         stt_client = STT_Engine()
#         stt_client.reading_thread = threading.Thread(target=stt_client.listen)
#         stt_client.reading_thread.start()
#         input()
#     finally:
#         stt_client.close()
#
# if __name__ == "__main__":
#     main()
