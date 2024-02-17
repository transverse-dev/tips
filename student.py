import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from MeetingSummary.main import MeetingSummary

ms = MeetingSummary()

f = open("Recording.txt", 'a', encoding='UTF-8')

st.title("Audio Demo")
st.write("Student screen")


def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    if ms.recording(frame.sample_rate, frame.to_ndarray()[0]) : # sample_rate, raw_sound(WAV)
            ms.summary() # 40초마다 요약
            f.write('translated: ' + ms.translated_txt + '\n')
            f.write('summarized: ' + ms.summarized_txt + '\n\n')
    return frame
    

webrtc_streamer(key="Demo", audio_frame_callback=audio_frame_callback)