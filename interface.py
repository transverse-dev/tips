
import gradio as gr
import numpy as np
from STT import transcribe, chunk_processing
from GPT import GPTf

# 회의 전체 내용 보관
TEXT_HISTORY = []
summary = "초기 녹음"

def STTandGPT(sr, stream):

    print("STT & GPT functions are called")

    # stt 실행
    stt = transcribe(sr, stream)
    TEXT_HISTORY.append(stt)
    summary = GPTf(stt, TEXT_HISTORY)

    print("stt 실행: ", len(stream))
    print(stt)              ## STT 성능 확인용
    return None, summary
    

def summarySpeech(stream, new_chunk):
    global summary

    # 청크 소리파형 전처리
    sr, y = chunk_processing(new_chunk)

    # 말 단위 조합해서 문장 만들기
    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y

    print(len(stream))

    if len(stream) == 2400000: #24000Hz * 100
        # 5초마다 타이머 실행
        stream, summary = STTandGPT(sr, stream)

    return stream, summary
        


input_audio = gr.Audio(
    sources=["microphone", 'upload'],
    waveform_options=gr.WaveformOptions(
        waveform_color="#01C6FF",
        waveform_progress_color="#0066B4",
        skip_length=2,
        show_controls=False,
    ),
    streaming=True,
)


# 우선 클릭해서 녹음하는 형태로 Start. 나중에 Streaming 형태로 만들자.
demo = gr.Interface(
    fn=summarySpeech,
    inputs=["state", input_audio],
    outputs=["state","text"],
    live=True,
)

if __name__ == "__main__":
    demo.launch()