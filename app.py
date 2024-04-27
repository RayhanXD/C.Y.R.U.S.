import csv
import copy
import argparse
from collections import Counter
from collections import deque
from lightbars import *
from functions import *
from preprocess import *
from draw import *
from gesture_logging import calc_bounding_rect, calc_landmark_list

import cv2 as cv
import mediapipe as mp

from model import KeyPointClassifier
from model import PointHistoryClassifier

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=540)
    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence", type=float, default=1)
    parser.add_argument("--min_tracking_confidence", type=int, default=0.7)
    args = parser.parse_args()
    return args

mp_hands_instance = None
keypoint_classifier_instance = None
point_history_classifier_instance = None
cvFpsCalc_instance = None
history_length = 16
point_history = deque(maxlen=history_length)
finger_gesture_history = deque(maxlen=history_length)
mode = 0
showBrect = False
showInfo = False
drawPoint = True
drawLine = True

def process_frame(input_frame, showBrect, showInfo, drawPoint, drawLine, use_static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.5):
    global mp_hands_instance, keypoint_classifier_instance, point_history_classifier_instance, cvFpsCalc_instance
    global point_history, finger_gesture_history, mode

    if mp_hands_instance is None:
        mp_hands_instance = mp.solutions.hands.Hands(static_image_mode=use_static_image_mode, max_num_hands=6, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)
        keypoint_classifier_instance = KeyPointClassifier()
        point_history_classifier_instance = PointHistoryClassifier()

    hands = mp_hands_instance
    keypoint_classifier = keypoint_classifier_instance
    point_history_classifier = point_history_classifier_instance

    with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = [row[0] for row in csv.reader(f)]
    with open('model/point_history_classifier/point_history_classifier_label.csv', encoding='utf-8-sig') as f:
        point_history_classifier_labels = [row[0] for row in csv.reader(f)]

    image = cv.flip(input_frame, 1)
    final_image = copy.deepcopy(image)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    if results.multi_hand_landmarks is not None:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            brect = calc_bounding_rect(final_image, hand_landmarks)
            landmark_list = calc_landmark_list(final_image, hand_landmarks)
            pre_processed_landmark_list = pre_process_landmark(landmark_list)
            pre_processed_point_history_list = pre_process_point_history(final_image, point_history)
            
            hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
            if hand_sign_id == 2:
                point_history.append(landmark_list[8])
            else:
                point_history.append([0, 0])
            if hand_sign_id in hand_sign_functions:
                hand_sign_functions[hand_sign_id]()
            finger_gesture_id = 0
            point_history_len = len(pre_processed_point_history_list)
            if point_history_len == (history_length * 2):
                finger_gesture_id = point_history_classifier(pre_processed_point_history_list)
# Now you can check if the finger gesture ID is in the dictionary and call the function

            finger_gesture_history.append(finger_gesture_id)
            most_common_fg_id = Counter(finger_gesture_history).most_common()

            most_common_fg_id = Counter(finger_gesture_history).most_common(1)
            if most_common_fg_id:
                # Extract the finger gesture ID from the first tuple
                finger_gesture_id = most_common_fg_id[0][0]
                # Convert finger_gesture_id to int before the lookup
                finger_gesture_id = int(finger_gesture_id)

            # print("Finger Gesture ID:", finger_gesture_id, type(finger_gesture_id))
            # print("Dictionary keys:", finger_gesture_functions.keys())

            final_image = draw_bounding_rect(showBrect, final_image, brect)
            final_image = draw_landmarks(final_image, landmark_list, drawPoint, drawLine)
            final_image = draw_info_text(final_image, showInfo, brect, handedness, keypoint_classifier_labels[hand_sign_id], point_history_classifier_labels[most_common_fg_id[0][0]])

    else:
        point_history.append([0, 0])

    final_image = draw_point_history(final_image, point_history)

    return final_image
