import streamlit as st
from streamlit_webrtc import webrtc_streamer
from CV.interface import CV
import av

st.title("CV Demo")
st.write("Presenter screen")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    changed_img = CV(img)
    return av.VideoFrame.from_ndarray(changed_img, format="bgr24")

webrtc_streamer(key="example", video_frame_callback=video_frame_callback)