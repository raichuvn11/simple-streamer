import threading
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="WebRTC", layout="wide")

col1,col2 = st.columns(2)

lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return 


with col1:
    ctx = webrtc_streamer(
        key="example",
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={
            "iceServers": [
                {
                    "urls": ["turn:relay1.expressturn.com:3478"],
                    "username": "efFOT2XDG4ORX9KD73",
                    "credential": "5UlhzC61tHCk4gH5"
                }
            ]
        }
    )


imgout_place = col2.empty()


while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    # phát hiện khuôn mặt, đóng khung 
    imgout = cv2.flip(img, 0)

    imgout_place.image(imgout, channels="BGR")
