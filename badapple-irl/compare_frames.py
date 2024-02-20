# workflow to compare the frames I took on the camera with the frames I needed to take, side by side. Basically, if I go
# forward 100 frames in this worfklow, and see that the frames don't match, I know that I had a mistake somewhere.
# if I had too many pictures, I just delete the picture and rerun the script. If I'm missing a picture, I made
# a copy of a similar picture for now, while I process all the frames. Later, I went and redid the frames I was missing
# (missing_frames.py) to figure out which pictures I had to take
import streamlit as st
import os
import cv2
frame_number = st.number_input('Enter frame number', min_value=0, max_value=3104, value=0, step=1)
rotation_number = st.number_input("Rotation", min_value=0, max_value=270, value=0, step=90)
col1, col2 = st.columns(2)
true_frame_path = "badapple-irl/circle_frames"
frames_taken = r"K:\badapple-frames"
all_images_in_frames_taken = os.listdir(frames_taken)
# filter by JPG only
all_images_in_frames_taken = [i for i in all_images_in_frames_taken if i.endswith(".JPG")]

permutation = [int(x.strip()) for x in open("badapple-irl/permutation.txt", "r").readlines()]
first_placeholder = col1.empty()
second_placeholder = col2.empty()


true_frame = f"{true_frame_path}/{permutation[frame_number]}.jpg"
actual_frame = os.path.join(frames_taken, all_images_in_frames_taken[frame_number])
actual = cv2.imread(actual_frame)
actual = cv2.cvtColor(actual, cv2.COLOR_BGR2RGB)

if rotation_number != 0:
    actual = cv2.rotate(actual, rotation_number//90-1)
first_placeholder.image(true_frame, use_column_width=True)
second_placeholder.image(actual, use_column_width=True)

st.write(true_frame, "vs",  actual_frame)


