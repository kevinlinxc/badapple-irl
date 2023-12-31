import streamlit as st
import os
from pathlib import Path
from PIL import Image  # https://github.com/streamlit/streamlit/issues/1294#issuecomment-1488435694

# dupes found by find_duplicate_frames.py

st.set_page_config(layout="centered")

hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# original_expander = st.expander("Original frame")
frame_number = st.number_input('Enter frame number', min_value=0, max_value=6572, value=0, step=1)

row1_text = st.empty()
row1 = st.empty()
row2_text = st.empty()
row2 = st.empty()
# let user manually enter image number, or click next and back


# display images from real_frames, circle_frames and diff_frames based on image number
base = Path("badapple-irl").resolve()
# real_path = base / "real_frames" / f"{frame_number}.jpg"
# if os.path.exists(real_path):
#     img = Image.open(real_path)
#     original_expander.image(img)

circle_path = base / "circle_frames_opt" / f"{frame_number}.jpg"
if os.path.exists(circle_path):
    row2_text.write(f"Frame {frame_number}")
    img = Image.open(circle_path)
    row2.image(img)


diff_path = base / "diff_frames_opt" / f"{frame_number}.jpg"
if os.path.exists(diff_path):
    # row1_text.write(f"Frames {frame_number-1} to {frame_number} diff")
    img = Image.open(diff_path)
    row1.image(img)



