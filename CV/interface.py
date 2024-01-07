import cv2

# 웹캠 캡처 객체 생성
cap = cv2.VideoCapture(0)

# 웹캠 해상도 설정 (원하는 해상도로 조절)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # 여기에서 추가적인 프레임 처리를 할 수 있음
    # ...

    # 프레임을 화면에 표시
    cv2.imshow("Webcam", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 프로그램 종료 시 웹캠 객체 해제
cap.release()

# OpenCV 창 닫기
cv2.destroyAllWindows()
