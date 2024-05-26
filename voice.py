import openai
from playsound import playsound
from itertools import cycle

# client = OpenAI()
api_key = "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"

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

