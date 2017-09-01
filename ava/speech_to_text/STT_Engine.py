from watson_developer_cloud import SpeechToTextV1
import asyncio

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
    async def recognize(self, stream, queue_manager):
        message = self.stt.recognize(
            stream, content_type='audio/wav', timestamps=True,
            word_confidence=True)
        try:
            if message["results"][0]["alternatives"][0]["transcript"] :
                queue_manager.queue_command.put(message["results"][0]["alternatives"][0]["transcript"])
                queue_manager.queue_input.task_done()
                queue_manager.queue_tts.put("Okay")
        except:
            queue_manager.queue_tts.put("Retry your command please")
