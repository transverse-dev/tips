import cv2
from gazeTracking.gazeTracking import GazeTracking
from warning import print_face, print_jawline

def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    gaze = GazeTracking()

    while True:
        _, frame = cap.read()

        # gaze_tracking 눈동자 표시
        gaze.refresh(frame)
        new_frame = gaze.annotated_frame()

        # 눈동자 좌/우 편향시 빨간색으로 얼굴 표시
        if gaze.is_right() or gaze.is_left():
            print_face(new_frame)
        
        # 고개가 돌아가면 보라색으로 표시
        print_jawline(new_frame)

        cv2.imshow("Demo", new_frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
   main()