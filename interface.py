
import gradio as gr
from STT import STTf
from GPT import GPTf

# 회의 전체 내용 보관
TEXT_HISTORY = []

def summarySpeech(audio):
    # sr, data = audio
    stt = STTf(audio)
    TEXT_HISTORY.append(stt)
    summary = GPTf(stt, TEXT_HISTORY)
    return (summary)


input_audio = gr.Audio(
    sources=["microphone", 'upload'],
    waveform_options=gr.WaveformOptions(
        waveform_color="#01C6FF",
        waveform_progress_color="#0066B4",
        skip_length=2,
        show_controls=False,
    ),
)


# 우선 클릭해서 녹음하는 형태로 Start. 나중에 Streaming 형태로 만들자.
demo = gr.Interface(
    fn=summarySpeech,
    inputs=input_audio,
    outputs="text"
)

if __name__ == "__main__":
    demo.launch()