import cv2
import numpy as np
from pathlib import Path

badapple_path = Path("badapple-irl").resolve().parent / "badapple-small.mp4"

cap = cv2.VideoCapture(str(badapple_path))

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"width: {width}, height: {height}, fps: {fps}, n_frames: {n_frames}")
square_side = 40


ret, frame = cap.read()
frame_count = 0
last_frame_pixels = set()
total_min_moves = 0

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break
    # convert to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if frame_count % 100 == 0:
        print(f"frame {frame_count}/{n_frames}")
    frame_count += 1

    current_frame_pixels = set()
    for i in range(0, width - 1, square_side):
        for j in range(0, height - 1, square_side):
            section = frame[j : j + square_side, i : i + square_side]
            if (np.mean(section)) < 50:
                current_frame_pixels.add((i, j))
    # any time we move an apple from a place that was black on the last frame, and we have a formerly white spot that
    # needs an apple, we can save on a move by moving the apple from the black spot to the white spot.
    # this way, we can often halve the number of moves needed. I'm pretty sure it works out mathematically
    # that the quantity I'm looking for at each step is the maximum(white to black, black to white). The lower one
    # has all its needs filled by the higher one, and then the higher one has extra moves left over.
    moves_to_make = max(
        len(current_frame_pixels.difference(last_frame_pixels)),
        len(last_frame_pixels.difference(current_frame_pixels)),
    )
    print(f"Frame {frame_count} to {frame_count+1} had {moves_to_make} moves")
    total_min_moves += moves_to_make
    last_frame_pixels = current_frame_pixels


print(f"Total min moves: {total_min_moves}")
