import streamlit as st
import os
from pathlib import Path
from PIL import (
    Image,
)  # https://github.com/streamlit/streamlit/issues/1294#issuecomment-1488435694

# dupes found by find_duplicate_frames.py
dupes = [97, 98, 103, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 419, 451, 465, 466, 467, 469, 470, 471, 489, 490, 502, 503, 504, 505, 506, 507, 642, 653, 654, 667, 679, 732, 733, 1143, 1145, 1146, 1150, 1154, 1155, 1156, 1163, 1362, 1550, 1551, 1552, 1553, 1554, 1555, 2248, 2352, 2358, 2378, 2379, 2498, 2499, 2500, 2584, 2593, 2655, 2656, 2657, 2658, 2659, 2660, 2661, 2662, 2663, 2664, 2665, 2666, 2667, 2668, 2669, 2670, 2671, 2672, 2673, 2810, 2817, 2821, 2876, 2877, 2878, 2879, 2880, 2881, 2883, 2910, 2943, 2944, 2945, 2946, 2947, 2948, 2949, 2950, 2951, 2952, 2953, 2954, 2955, 2956, 2957, 2958, 2959, 2963, 3082]
dupe_set = set(dupes)

st.set_page_config(layout="centered")

hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# original_expander = st.expander("Original frame")
frame_number = st.number_input(
    "Enter frame number", min_value=0, max_value=3104, value=0, step=1
)
warning_area = st.empty()
if frame_number in dupe_set:
    warning_area.warning("This frame is a duplicate")
else:
    warning_area.empty()
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

circle_path = base / "circle_frames_opt" / f"{frame_number}.png"
if os.path.exists(circle_path):
    row2_text.write(f"Frame {frame_number}")
    img = Image.open(circle_path)
    row2.image(img)


diff_path = base / "diff_frames_opt" / f"{frame_number}.png"
if os.path.exists(diff_path):
    # row1_text.write(f"Frames {frame_number-1} to {frame_number} diff")
    img = Image.open(diff_path)
    row1.image(img)
