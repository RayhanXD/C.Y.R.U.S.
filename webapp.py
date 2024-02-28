from flask import Flask, Response, request, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
import requests
from openai import OpenAI
import os
import cv2 as cv
from app import process_frame

app = Flask(__name__)

def generate():
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = process_frame(frame)
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
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": transcript["text"]
            }
        ],
        max_tokens=300,
        stream=True
    )
    
    socketio.emit('user_text', {'data': transcript['text']})

    for chunk in chat_response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content)
            socketio.emit('chatbot_text', {'data': chunk.choices[0].delta.content})

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)