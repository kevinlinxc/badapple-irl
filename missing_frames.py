# i used compare_frames.py, a streamlit workflow to figure out which frames I was missing. I copied and pasted
# other frames to fill the gaps temporarily, to mark which frames I was missing and to make it much easier
# to keep finding the missing frames. This script is to point out all the missing frames
import os
from pathlib import Path
import cv2

true_frame_path = Path(__file__).resolve().parent / "circle_frames"
frames_taken = r"K:\badapple-frames"
all_images_in_frames_taken = os.listdir(frames_taken)
# filter by JPG only
all_images_in_frames_taken = [
    i for i in all_images_in_frames_taken if i.endswith(".JPG")
]

permutation = [int(x.strip()) for x in open("permutation.txt", "r").readlines()]

# cv2 show the circle_frames where the zipped corresponding frame_taken has the word "copy" in its name
print(all_images_in_frames_taken)
print(permutation)
zipped = list(zip(all_images_in_frames_taken, permutation))
print(zipped)

for i in zipped:
    if "Copy" in i[0]:
        frame_that_needs_redo = f"{true_frame_path}/{i[1]}.jpg"
        frame = cv2.imread(frame_that_needs_redo)
        # save with the copy name but add "needed"
        cv2.imwrite(f"{i[1]}_needed.png", frame)
        print(f"Wrote {i[1]}_needed.png")
