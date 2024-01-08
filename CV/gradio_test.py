
################
# Gradio는 비디오 송출이 너무 느려서 Real-Time Streaming이 불가합니다.
# CV2로 툴을 바꿔서 작업하겠습니다.
################


import cv2
import gradio as gr

# 웹캠 캡처 객체 생성
cap = cv2.VideoCapture(0)

# 웹캠 해상도 설정 (원하는 해상도로 조절)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def process_image(_):
    # 여기에서 웹캠 프레임을 사용하여 이미지 처리를 수행
    # 이 예제에서는 텍스트를 받아와서 OpenCV 창에 표시

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        return None
    
    # 이미지 크기를 반으로 줄임
    frame = cv2.resize(frame, (320, 240))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, "text_input"

# Gradio 웹 인터페이스 정의
with gr.Blocks() as demo:
    with gr.Row():
        input_audio = gr.Audio()
        image = gr.Image(streaming=True)
        output = gr.Text()
        input_audio.stream(process_image, [input_audio], [image, output]) # , every=0.1 -> frame 높아지지만 서버 강제종료


# Gradio 웹 인터페이스 실행
demo.queue().launch()

# 프로그램 종료 시 웹캠 객체 해제
cap.release()
