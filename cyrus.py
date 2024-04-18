from openai import OpenAI
from flask_socketio import SocketIO
from voice import voice
import subprocess
import socketio

client = OpenAI()
socketio = SocketIO()
app_process = None

activate = "search google chrome for youtube"

def execute_command(activate):
    wraps = True
    chat_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "your name is C.Y.R.U.S.. you stand for Cybernetic Responsive Utility System. your task is to process commands like 'open calculator,' 'open notes,' and 'open chrome,' translating them into zsh terminal functions that execute the application. Be simple and do not provide any access words, simply only the terminal command. If the prompt is not a terminal command, then response as if you are a normal chatbot, however, try your best to convert and detect all commands. You are allowed to use AppleScript to perform more complex tasks. Remember, be simple and do not be excessive. make sure the commands are optimal for MacOS applications"
            },
            {
                "role": "user",
                "content": activate['text']
            }
        ]
    )

    code = chat_response.choices[0].message.content
    try:
        subprocess.run(code, shell=True, executable="/bin/bash", check=True)
    except subprocess.CalledProcessError:
        code = "Invalid Command, try something else?"
        wraps = False
    
    vocal_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Your name is Cyrus. your task is to convert the terminal command given in the prompt and convert it to normal words. Give me the words in verb tense, to where you are performing the action. For example, if the command given was 'open -a Maps' then you would say 'opening maps'. Be simple but also have a conversation with the user if prompted to do so. Never repeat the terminal command and always convert it into plain english. if there is an error, summarize the error."
            },
            {
                "role": "user",
                "content": code
            }
        ],
        max_tokens=300,
    )
    
    input = vocal_response.choices[0].message.content
    voice(input, wraps)

    return input
