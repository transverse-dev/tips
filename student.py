import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from MeetingSummary.main import MeetingSummary

ms = MeetingSummary()

st.title("Audio Demo")
st.write("Student screen")

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    return frame

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    if ms.recording(frame.sample_rate, frame.to_ndarray()) : # sample_rate, raw_sound
            ms.summary() # return 값이 True일 경우 실행 = 10000개 chunk마다 실행
            print(ms.translated_txt)
            print()
            print(ms.summarized_txt)
            # st.write(ms.translated_txt)
            # st.empty()
            # st.write(ms.summarized_txt)
    

ctx = webrtc_streamer(key="Demo", 
                      video_frame_callback=video_frame_callback,
                      audio_frame_callback=audio_frame_callback)