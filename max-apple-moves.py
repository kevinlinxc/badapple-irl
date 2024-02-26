import cv2
import numpy as np
from pathlib import Path

badapple_path = Path(".").resolve() / "badapple-small.mp4"

cap = cv2.VideoCapture(str(badapple_path))

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

square_side = 30
frame_start = 365
n_frames = int((cap.get(cv2.CAP_PROP_FRAME_COUNT)-frame_start)/2)
print(f"width: {width}, height: {height}, fps: {fps}, n_frames: {n_frames}")

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
ret, frame = cap.read()
frame_count = 0
last_frame_pixels = set()
total_max_moves = 0

while cap.isOpened():
    ret, frame = cap.read()
    ret, frame = cap.read() # skip a frame because 15 fps
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # if frame_count % 100 == 0:
    #     print(f"frame {frame_count}/{n_frames}")
    frame_count += 1

    current_frame_pixels = set()
    for i in range(0, width - 1, square_side):
        for j in range(0, height - 1, square_side):
            section = frame[j : j + square_side, i : i + square_side]
            if (np.mean(section)) < 50:
                current_frame_pixels.add((i, j))
    # the maximum number of moves is from removing all apples that go from black to white,
    # and adding all apples that go from white to black. So, I need the exclusive or of the two sets.
    # I say maximum because an optimized solution moves apples from a former black spot to a future black spot,
    # but for this script I just want to know an upper bound.
    moves = current_frame_pixels ^ last_frame_pixels
    print(f"Frame {frame_count} to {frame_count+1} had {len(moves)} moves")
    # print(f"White to black: {current_frame_pixels.difference(last_frame_pixels)}")
    # print(f"Black to white: {last_frame_pixels.difference(current_frame_pixels)}")
    total_max_moves += len(moves)
    last_frame_pixels = current_frame_pixels


print(f"Total max moves: {total_max_moves}")
