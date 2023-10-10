import streamlit as st
import os
from pathlib import Path

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
# let user manually enter image number, or click next and back

frame_number = st.number_input('Enter frame number', min_value=1, max_value=6572, value=1, step=1)

# display images from real_frames, circle_frames and diff_frames based on image number
base = Path("downsampling").resolve()
real_path = base / "real_frames" / f"{frame_number}.jpg"
print(real_path)
if os.path.exists(real_path):
    col1.image(str(real_path))

circle_path = base / "circle_frames" / f"{frame_number}.jpg"
print(circle_path)
if os.path.exists(circle_path):
    col2.image(str(circle_path))


