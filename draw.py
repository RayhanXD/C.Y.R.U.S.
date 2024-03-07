import cv2 as cv

def draw_landmarks(image, landmark_point, drawPoint, drawLine):
    if len(landmark_point) > 0:
        # Thumb
        if drawLine:
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (165, 116, 34), 3)

            # Index finger
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (165, 116, 34), 3)

            # Middle finger
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (165, 116, 34), 3)

            # Ring finger
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (165, 116, 34), 3)

            # Little finger
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (165, 116, 34), 3)

            # Palm
            cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (165, 116, 34), 3)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (165, 116, 34), 3)

    # Key Points
    if drawPoint:
        for index, landmark in enumerate(landmark_point):
            if index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:  # Joints excluding fingertips
                cv.circle(image, (landmark[0], landmark[1]), 10, (148, 75, 187), -1)

    return image

def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # Outer rectangle
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 0, 0), 2)

    return image

def draw_info_text(image, show, brect, handedness, hand_sign_text,
                   finger_gesture_text):

        if show:
                cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 25),
                 (0, 0, 0), 2)
                    
                info_text = handedness.classification[0].label[0:]
                if hand_sign_text != "":
                        info_text = info_text + ':' + hand_sign_text
                cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
                        cv.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0), 2, cv.LINE_AA)

                cv.putText(image, "Finger Gesture:" + finger_gesture_text, (100, 60),
                                cv.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0), 2,
                                cv.LINE_AA)

                return image
        else: 
             return image

def draw_point_history(image, point_history):
    for index, point in enumerate(point_history):
        if point[0] != 0 and point[1] != 0:
            cv.circle(image, (point[0], point[1]), 2 + int(index/2),
                      (0, 0, 0), 1)

    return image