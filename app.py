import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import threading

from MeetingSummary.main import MeetingSummary
from CV.main import CV

## Initialize objects
ms = MeetingSummary()

def summary_thread():
    ms.summary()

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    if ms.recording(frame.sample_rate, frame.to_ndarray()[0]):
        threading.Thread(target=summary_thread).start()
    return frame

def video_frame_callback(frame):
    changed_img = CV(frame.to_ndarray(format="bgr24"))
    return av.VideoFrame.from_ndarray(changed_img, format="bgr24")

## streamlit
st.title("Demo")
layout1, layout2 = st.columns([0.5, 0.5])

with layout1:
    st.write("Presenter screen")
    webrtc_streamer(key="Presenter", audio_frame_callback=audio_frame_callback)

with layout2:
    st.write("Student screen")
    webrtc_streamer(key="Student1", video_frame_callback=video_frame_callback)
