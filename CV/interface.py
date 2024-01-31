import cv2
import dlib
from gazeTracking.gazeTracking import GazeTracking
from warning import Warning

def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    gaze = GazeTracking()
    warning = Warning()
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("CV\shape_predictor_68_face_landmarks.dat")

    while True:
        _, frame = cap.read()
        new_frame = frame

        #전처리
        gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        facial_landmarks = []
        for face in faces:
           facial_landmarks.append(predictor(gray, face))
        
        # Eyetracking & 고개각도
        if facial_landmarks:
            gaze.refresh(new_frame, faces[0], facial_landmarks[0])
            # gaze_tracking 눈동자 표시
            new_frame = gaze.annotated_frame()
            warning.refresh(new_frame, faces[0], facial_landmarks[0])
            # 눈동자 좌/우 편향시 빨간색으로 얼굴 표시
            if gaze.is_right() or gaze.is_left():
                new_frame = warning.eyetracking_warning()
            # 턱선 좌/우 편향시 표시
            new_frame = warning.jawline_warning()

        cv2.imshow("Demo", new_frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
   main()