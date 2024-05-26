import openai
from playsound import playsound
from itertools import cycle
from dotenv import load_dotenv
import os

# client = OpenAI()
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

strings = ['Of course, Rayhan. ', 'Okay, Rayhan. ', '']

def cycle_strings():
    return next(cycled_strings)
    
cycled_strings = cycle(strings)

embed = True

def voice(input, embed):

    if embed:
        input = cycle_strings() + input
    else:
        input = input

    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input= input,
    )

    response.stream_to_file("output.mp3")
    playsound("output.mp3")

