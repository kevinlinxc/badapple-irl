# make movie using opencv
import cv2
from pathlib import Path
import os

circle_frames_path = Path(".").resolve() / "circle_frames"

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# get all the file names
files = os.listdir(circle_frames_path)
# sort them by number
files.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
# open one file to get the width and height
frame = cv2.imread(str(circle_frames_path / files[0]))
height, width, layers = frame.shape
print(f"width: {width}, height: {height}")
# get fps of bad_apple_small.mp4
vid_path = Path(".").resolve().parent / "badapple-small.mp4"
cap = cv2.VideoCapture(str(vid_path))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f"fps: {fps}")
# for i from 1 to 3, try doing every ith frame instead of all of them to see how they look
for i in range(1, 4):
    out = cv2.VideoWriter(f"circle{i}.mp4", fourcc, fps / i, (960, 720))
    for file in files[::i]:
        print(f"i: {i}, file: {file}", end="\r", flush=True)
        frame = cv2.imread(str(circle_frames_path / file))
        out.write(frame)
    print(f"Done {i}")
    out.release()
