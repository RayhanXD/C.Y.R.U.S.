import requests
import time
from voice import voice

API_KEY = '3c42ae12-da77-4165-8ff7-29a3227bd666'
DEVICE_ID = 'F2:7B:CC:35:34:37:68:14'
BASE_URL = 'https://developer-api.govee.com/v1/devices/control'

headers = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}

light_on = True

request_count = 0
start_time = time.time()

def light_switch():
    global light_on, request_count, start_time
    current_time = time.time()  

    if current_time - start_time > 60:
        request_count = 0
        start_time = current_time
    
    request_count += 1

    if request_count >= 9:
        return "Limit Reached"
    
    message = "Lights turning off" if light_on else "Lights turning on"
    voice(message)  # Call the voice function with the message

    if light_on:
        turn_off_light()
        light_on = False
        return "Gesture = Light OFF"
    else:
        turn_on_light()
        light_on = True
        return "Gesture = Light ON"

def turn_on_light():
    payload = {
        "device": DEVICE_ID,
        "model": "H6056",
        "cmd": {
            "name": "turn",
            "value": "on"
        }
    }
    response = requests.put(BASE_URL, json=payload, headers=headers)
    return response.text

def turn_off_light():
    payload = {
        "device": DEVICE_ID,
        "model": "H6056",
        "cmd": {
            "name": "turn",
            "value": "off"
        }
    }
    response = requests.put(BASE_URL, json=payload, headers=headers)
    return response.text

color_counter = 0

def set_color():
    global light_on, request_count, start_time, color_counter
    current_time = time.time()
    
    if current_time - start_time > 60:
        request_count = 0
        start_time = current_time
    
    request_count += 1

    if request_count >= 9:
        return "Limit Reached"
    
    colors = [(0, 0, 255), (0, 255, 0), (128, 0, 128), (227, 255, 237)]
    color_names = ["BLUE", "GREEN", "PURPLE", "WHITE"]
    current_color = colors[color_counter % len(colors)]
    color_name = color_names[color_counter % len(color_names)]

    payload = {
        "device": DEVICE_ID,
        "model": "H6056",
        "cmd": {
            "name": "color",
            "value": {
                "r": current_color[0],
                "g": current_color[1],
                "b": current_color[2]
            }
        }
    }
    
    requests.put(BASE_URL, json=payload, headers=headers)
    
    color_counter += 1
    light_on = True
    
    message = f"Light color changing to {color_name}"
    voice(message)
    
    return f"Gesture = COLOR: {color_name}"

