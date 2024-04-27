from openai import OpenAI
from playsound import playsound
from itertools import cycle

client = OpenAI()

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

    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input= input,
    )

    response.stream_to_file("output.mp3")
    playsound("output.mp3")

