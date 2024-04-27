from flask import Flask, Response, request, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
from lightbars import *
from cyrus import *
from custom_lights import light_function
import requests
from openai import OpenAI
import os
import cv2 as cv
from app import process_frame, showBrect, showInfo, drawLine, drawPoint

app = Flask(__name__)

def generate():
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = process_frame(frame, showBrect, showInfo, drawPoint, drawLine)
        (flag, encodedImage) = cv.imencode(".jpg", frame)
        if not flag:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + 
               bytearray(encodedImage) + b'\r\n')

@app.route('/video_feed')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

client = OpenAI()

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def userVoice():
    audio_file = request.files['file']
    audio_file.save('audio.webm')

    with open('audio.webm', 'rb') as f:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": f},
            data={"model": "whisper-1"}
        )
    transcript = response.json()
    socketio.emit('user_text', {'data': transcript['text']})

    return transcript

app.config['UPLOAD_FOLDER'] = '/Users/rayhanmohammad/Desktop/GRWebTesting'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html') #reads HTML file from templates folder

@app.route('/upload', methods=['POST'])
def upload():
    audio_file = request.files['file']
    audio_file.save('audio.webm')

    # Now you can use the saved audio file for further processing
    with open('audio.webm', 'rb') as f:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": f},
            data={"model": "whisper-1"}
        )
    transcript = response.json()

    # Send the transcribed text to the ChatCompletion API
    chat_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "C.Y.R.U.S. (Cybernetic Responsive Utility System) is an advanced AI assistant designed to optimize both personal and professional tasks through its powerful, multifunctional capabilities. It excels in data analysis, offering detailed insights to aid in decision-making, automates routine tasks to enhance productivity, and manages real-time communication across diverse platforms to ensure seamless collaboration. Additionally, C.Y.R.U.S. integrates robust security features to monitor and protect against both digital and physical threats, making it an indispensable tool for modern, efficient operations."
            },
            {
                "role": "user",
                "content": transcript["text"]
            }
        ],
        max_tokens=1000,
        stream=True
    )

    socketio.emit('user_text', {'data': transcript['text']})


    for chunk in chat_response:
        if chunk.choices[0].delta.content is not None:
            socketio.emit('chatbot_text', {'data': chunk.choices[0].delta.content})

    return '', 200

@app.route('/cyrus', methods=['POST'])
def cyrus():
    
    transcript = userVoice()

    feedback = execute_command(transcript)
    socketio.emit('chatbot_text', {'data': feedback})

    return '', 200

@app.route('/light', methods=['POST'])
def lightcontrol():

    transcript = userVoice()
    command = transcript['text']
    
    feedback = light_function(command)
    socketio.emit('chatbot_text', {'data': feedback})

    return '', 200
    
@app.route('/silent', method=['POST'])
def zapierWorkflow():
    # Your Zapier webhook URL
    webhook_url = 'https://hooks.zapier.com/hooks/catch/18087776/3njjmbi/'

    # Data you want to send
    data = {
        'recipient': 'backup7867rm@gmail.com',
        'subject': 'Hello from Your AI Assistant',
        'body': 'Here is the information you requested...'
    }

    # Make a POST request
    response = requests.post(webhook_url, json=data)

    # Check response status
    if response.status_code == 200:
        print('Data sent successfully')
    else:
        print('Failed to send data: Status code', response.status_code)

@app.route('/update_showBrect', methods=['POST'])
def update_showBrect():
    global showBrect
    showBrect = request.form.get('showBrect') == 'true'
    return "Brect Shown Toggled"

@app.route('/update_showInfo', methods=['POST'])
def update_showInfo():
    global showInfo
    showInfo = request.form.get('showInfo') == 'true'
    return "Info Shown Toggled"

@app.route('/update_drawPoint', methods=['POST'])
def update_drawPoint():
    global drawPoint
    drawPoint = (request.form.get('drawPoint') == 'true')
    return "Points Toggled"

@app.route('/update_drawLine', methods=['POST'])
def update_drawLine():
    global drawLine
    drawLine = (request.form.get('drawLine') == 'true')
    return "Lines Toggled"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)