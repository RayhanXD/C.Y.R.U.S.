from openai import OpenAI
from playsound import playsound
import warnings

warnings.filterwarnings("ignore", message="Due to a bug, this method doesn't actually stream the response content")

client = OpenAI()

def voice(input):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input,
    )

    response.stream_to_file("output.mp3")
    playsound("output.mp3")

