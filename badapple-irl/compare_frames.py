import streamlit
import os

col1, col2 = streamlit.columns(2)
true_frame_path = "badapple-irl/circle_frames_opt"
frames_taken = r"K:\badapple-frames"
all_images_in_frames_taken = os.listdir(frames_taken)
# filter by JPG only
all_images_in_frames_taken = [i for i in all_images_in_frames_taken if i.endswith(".JPG")]


first_placeholder = col1.empty()
second_placeholder = col2.empty()

for i in range(3104):
    true_frame = f"{true_frame_path}/{i}.png"
    first_placeholder.image(true_frame, use_column_width=True)
    second_placeholder.image(all_images_in_frames_taken[i], use_column_width=True)



