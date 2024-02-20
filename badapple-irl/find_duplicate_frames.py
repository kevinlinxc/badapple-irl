# after downsampling, there may be some frames that are duplicates of original frames. I want to print out a dictionary
# of all these frames, so I can later put the original frame in the place of the duplicate frame, and be able to skip
# arranging the apples for those frames

import cv2
import numpy as np
from pathlib import Path

badapple_path = Path(".").resolve().parent / "badapple-small.mp4"

cap = cv2.VideoCapture(str(badapple_path))

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"width: {width}, height: {height}, fps: {fps}, n_frames: {n_frames}")
square_side = 30


ret, frame = cap.read()
frame_count = 0
hashset = set()
hashmap = {}
duplicates = {}
total_duplicates = 0
flat_duplicates_list = []


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
    hash_of_frame = hash(frozenset(current_frame_pixels))
    if hash_of_frame in hashset:
        original_frame = hashmap[hash_of_frame]
        print(f"Frame {frame_count} is a duplicate of {original_frame}")
        duplicates[original_frame].append(frame_count)
        total_duplicates += 1
        flat_duplicates_list.append(frame_count)
    else:
        hashset.add(hash_of_frame)
        hashmap[hash_of_frame] = frame_count
        duplicates[frame_count] = []

print("All duplicates:")
print(duplicates)
print(f"Total duplicates: {total_duplicates}")
print(f"Flat duplicates list: {flat_duplicates_list}")
