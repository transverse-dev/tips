import dlib
import cv2
from CV.gazeTracking.gazeTracking import GazeTracking
from CV.warning import Warning

gaze = GazeTracking()
warning = Warning()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("CV\shape_predictor_68_face_landmarks.dat")


def CV(frame):
    global gaze, warning, detector, predictor

    #전처리
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    facial_landmarks = []
    if faces:
       facial_landmarks.append(predictor(gray, faces[0]))
    
    # Eyetracking & 고개각도
    if facial_landmarks:
        gaze.refresh(frame, faces[0], facial_landmarks[0])
        # gaze_tracking 눈동자 표시
        frame = gaze.annotated_frame()
        warning.refresh(frame, faces[0], facial_landmarks[0])
        # 눈동자 좌/우 편향시 빨간색으로 얼굴 표시
        if gaze.is_right() or gaze.is_left():
            frame = warning.eyetracking_warning()
        # 턱선 좌/우 편향시 표시
        frame = warning.jawline_warning()

    return frame