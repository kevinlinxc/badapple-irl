"""
Goal: downsample the video to a smaller resolution, then replace each small section of the video with a circle,
which will represent a real life apple on a white background.
"""

import cv2
import numpy as np
from pathlib import Path

# original video
badapple_path = Path(".") / "badapple-small.mp4"

cap = cv2.VideoCapture(str(badapple_path))

# get info
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"width: {width}, height: {height}, fps: {fps}, n_frames: {n_frames}")

# turn nxn pixel sections of the video into all black or all white
square_side = 30

# make a video writer
fourcc = cv2.VideoWriter_fourcc(*"avc1")
out = cv2.VideoWriter(
    f"circle_downsampled{square_side}-{square_side}small.mp4",
    fourcc,
    fps,
    (width, height),
)

ret, frame = cap.read()
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # convert to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if frame_count % 100 == 0:
        print(f"frame {frame_count}/{n_frames}")
    frame_count += 1
    # make a new blank image
    out_frame = np.ones((height, width), dtype=np.uint8) * 255
    # iterate over kernels of the frame
    for i in range(0, width - 1, square_side):
        for j in range(0, height - 1, square_side):
            # get section of frame
            section = frame[j : j + square_side, i : i + square_side]
            # if it's highly dark, replace with black circle
            if (np.mean(section)) < 50:
                cv2.circle(
                    out_frame,
                    (i + square_side // 2, j + square_side // 2),
                    square_side // 2,
                    0,
                    -1,
                )

    # write frame
    # display original and new frame with hconcat
    cv2.imshow("frame", np.hstack((frame, out_frame)))
    cv2.waitKey(1)
    out_frame = cv2.cvtColor(out_frame, cv2.COLOR_GRAY2BGR)
    out.write(out_frame)

out.release()
cap.release()
