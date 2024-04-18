from openai import OpenAI
from playsound import playsound

client = OpenAI()

counter = 0
strings = ['Of course, Rayhan, ', 'Okay, Rayhan, ', '']

def cycle_strings():
    global counter
    result = strings[counter % len(strings)]
    counter += 1
    return result

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

