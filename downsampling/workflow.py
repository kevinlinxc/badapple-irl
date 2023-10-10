import streamlit as st
import os
from pathlib import Path

st.set_page_config(layout="wide")
frame_number = st.number_input('Enter frame number', min_value=0, max_value=6572, value=0, step=1)
original_expander = st.expander("Original")
col1, col2 = st.columns(2)
# let user manually enter image number, or click next and back


# display images from real_frames, circle_frames and diff_frames based on image number
base = Path("downsampling").resolve()
real_path = base / "real_frames" / f"{frame_number}.jpg"
if os.path.exists(real_path):
    original_expander.image(str(real_path))

circle_path = base / "circle_frames" / f"{frame_number}.jpg"
if os.path.exists(circle_path):
    col1.write(f"Frame {frame_number}")
    col1.image(str(circle_path))

diff_path = base / "diff_frames" / f"{frame_number}.jpg"
if os.path.exists(diff_path):
    col2.write(f"Frames {frame_number-1} to {frame_number} diff")
    col2.image(str(diff_path))



