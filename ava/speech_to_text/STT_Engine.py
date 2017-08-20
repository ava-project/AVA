from watson_developer_cloud import SpeechToTextV1

# Speech-To-Text Engine

class STT_Engine():

    # Setting Watson Credentials in app
    def __init__(self):
        self.stt = SpeechToTextV1(
            username = '9d526cf4-63de-47da-be7d-e5662d3cd1a9',
            password = 'oWaCHHSTzjkO',
            x_watson_learning_opt_out=False
        )

    # Sending audio file to translate
    def recognize(self, stream):
        return self.stt.recognize(
            stream, content_type='audio/wav', timestamps=True,
            word_confidence=True)
