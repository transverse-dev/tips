import threading
import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("CV Demo")
st.write("Student screen")

lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return frame

ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

fig_place = st.empty()

while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    ### 아래 화면 추가(while doing)