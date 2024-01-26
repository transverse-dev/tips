import dlib
import numpy as np
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def print_jawline(_frame):
    gray = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if not faces:
        return 1, 1 # skip
    facial_landmarks = predictor(gray, faces[0])
    ## 턱선
    # right_jawline = np.array([(facial_landmarks.part(1).x, facial_landmarks.part(2).y),
    #                         (facial_landmarks.part(7).x, facial_landmarks.part(6).y)], np.int32)
    # left_jawline = np.array([(facial_landmarks.part(15).x, facial_landmarks.part(2).y),
    #                         (facial_landmarks.part(9).x, facial_landmarks.part(6).y)], np.int32)
    
    ## 코 기준 좌우 가로선
    right_jawline = np.array([(facial_landmarks.part(33).x, facial_landmarks.part(2).y),
                            (facial_landmarks.part(2).x, facial_landmarks.part(6).y)], np.int32)
    left_jawline = np.array([(facial_landmarks.part(33).x, facial_landmarks.part(2).y),
                            (facial_landmarks.part(14).x, facial_landmarks.part(6).y)], np.int32)

    right_jawline_length = distance(right_jawline[0], right_jawline[1])
    left_jawline_length = distance(left_jawline[0], left_jawline[1])

    #왼쪽을 보고 있으면 왼쪽 턱선을 빨간색으로 출력합니다.
    if left_jawline_length / right_jawline_length < 0.75:
        cv2.polylines(_frame, [right_jawline], True, (0, 255, 0), 3)
        cv2.polylines(_frame, [left_jawline], True, (255, 0, 255), 3)
    #오른쪽을 보고 있으면 오른쪽 턱선을 빨간색으로 출력합니다.
    elif right_jawline_length / left_jawline_length < 0.75:
        cv2.polylines(_frame, [right_jawline], True, (255, 0, 255), 3)
        cv2.polylines(_frame, [left_jawline], True, (0, 255, 0), 3)
    #정면을 보고 있으면 양쪽 턱선을 초록색으로 출력합니다.
    else:
        cv2.polylines(_frame, [right_jawline], True, (0, 255, 0), 3)
        cv2.polylines(_frame, [left_jawline], True, (0, 255, 0), 3)

    return
    
def print_face(_frame):

    gray = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if not faces:
        return None
    facial_landmarks = predictor(gray, faces[0])
    face_region = np.array([(facial_landmarks.part(0).x, facial_landmarks.part(0).y),
                            (facial_landmarks.part(1).x, facial_landmarks.part(1).y),
                            (facial_landmarks.part(2).x, facial_landmarks.part(2).y),
                            (facial_landmarks.part(3).x, facial_landmarks.part(3).y),
                            (facial_landmarks.part(4).x, facial_landmarks.part(4).y),
                            (facial_landmarks.part(5).x, facial_landmarks.part(5).y),
                            (facial_landmarks.part(6).x, facial_landmarks.part(6).y),
                            (facial_landmarks.part(7).x, facial_landmarks.part(7).y),
                            (facial_landmarks.part(8).x, facial_landmarks.part(8).y),
                            (facial_landmarks.part(9).x, facial_landmarks.part(9).y),
                            (facial_landmarks.part(10).x, facial_landmarks.part(10).y),
                            (facial_landmarks.part(11).x, facial_landmarks.part(11).y),
                            (facial_landmarks.part(12).x, facial_landmarks.part(12).y),
                            (facial_landmarks.part(13).x, facial_landmarks.part(13).y),
                            (facial_landmarks.part(14).x, facial_landmarks.part(14).y),
                            (facial_landmarks.part(15).x, facial_landmarks.part(15).y),
                            (facial_landmarks.part(16).x, facial_landmarks.part(16).y),
                            (facial_landmarks.part(24).x, facial_landmarks.part(18).y),
                            (facial_landmarks.part(19).x, facial_landmarks.part(23).y)], np.int32)

    cv2.polylines(_frame, [face_region], True, (0, 0, 255), 5)