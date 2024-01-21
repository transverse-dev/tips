import cv2
import numpy as np
import dlib

def print_face(facial_landmarks, _gray, _frame):
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
                            (facial_landmarks.part(18).x, facial_landmarks.part(18).y),
                            (facial_landmarks.part(23).x, facial_landmarks.part(23).y)], np.int32)

    cv2.polylines(_frame, [face_region], True, (0, 255, 255), 1)

def main():

    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        face = faces[0]

        landmarks = predictor(gray, face)
        print_face(landmarks, gray, frame)

        cv2.imshow("Webcam", frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
   main()