import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from MeetingSummary.main import MeetingSummary
from CV.main import CV

## function
ms = MeetingSummary()

f = open("Recording.txt", 'a', encoding='UTF-8')

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    if ms.recording(frame.sample_rate, frame.to_ndarray()[0]) : # sample_rate, raw_sound(WAV)
            ms.summary() # 40초마다 요약
            f.write('translated: ' + ms.translated_txt + '\n')
            f.write('summarized: ' + ms.summarized_txt + '\n\n')
    return frame
    
def video_frame_callback(frame):
    changed_img = CV(frame.to_ndarray(format="bgr24"))
    return av.VideoFrame.from_ndarray(changed_img, format="bgr24")


## streamlit
st.title("Demo")
layout1,layout2 = st.columns([0.5,0.5])

with layout1:
    st.write("Presenter screen")
    webrtc_streamer(key="Presenter", audio_frame_callback=audio_frame_callback)

with layout2:
    st.write("Student screen")
    webrtc_streamer(key="Student", video_frame_callback=video_frame_callback)