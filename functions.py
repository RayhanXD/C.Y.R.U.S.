import time
from lightbars import *
from app import *
import threading
from threading import Lock

last_time_called = 0
last_time_light_called = 0
is_light_thread_running = False

turn_on_light()

def check_time_and_print(message):
    global last_time_called
    current_time = time.time()
    if current_time - last_time_called > 1.5:
        print(message)
        last_time_called = current_time

light_time_lock = Lock()
stop_threads = threading.Event()

def check_light_time(func):
    global last_time_light_called, is_light_thread_running
    with light_time_lock:
        current_time = time.time()
        if current_time - last_time_light_called > 2.5:
            result = func()
            print(result)
            last_time_light_called = current_time
    is_light_thread_running = False
        

def function_for_gesture_1():
    check_time_and_print("Gesture = Close")

def function_for_gesture_2():
    check_time_and_print("Gesture = Pointer")

def function_for_gesture_3():
    global is_light_thread_running
    if not is_light_thread_running:
        is_light_thread_running = True
        thread = threading.Thread(target=check_light_time, args=(light_switch,))
        thread.start()

def function_for_gesture_4():
    global is_light_thread_running
    if not is_light_thread_running:
        is_light_thread_running = True
        thread = threading.Thread(target=check_light_time, args=(set_color,))
        thread.start()
    
def function_for_gesture_open():
    check_time_and_print("Gesture = Open")

def function_for_gesture_5():
    check_time_and_print("Gesture = Love")

def function_for_thumbsup():
    check_time_and_print('Gesture = Thumbs Up')

hand_sign_functions = {
    0: function_for_gesture_open,
    1: function_for_gesture_1,
    2: function_for_gesture_2,
    3: function_for_gesture_3,
    4: function_for_gesture_4,
    5: function_for_gesture_5,
    6: function_for_thumbsup
}


#FINGER GESTURE FUNCTIONS

def check_finger_and_print(message):
    global last_time_called
    current_time = time.time()
    if current_time - last_time_called > 1.5:
        print(message)
        last_time_called = current_time

def function_for_finger_gesture_0():
    check_finger_and_print("Finger Gesture = Gesture Zero")

def function_for_finger_gesture_1():
    check_finger_and_print("Finger Gesture = Gesture One")

def function_for_finger_gesture_2():
    check_finger_and_print("Finger Gesture = Gesture Two")

def function_for_finger_gesture_3():
    check_finger_and_print("Finger Gesture = Gesture Three")

# Add more functions for each finger gesture as neede
# Map finger gesture IDs to their corresponding functions
finger_gesture_functions = {
    0: function_for_finger_gesture_0,
    1: function_for_finger_gesture_1,
    2: function_for_finger_gesture_2,
    3: function_for_finger_gesture_3
    # Add more mappings as needed
}