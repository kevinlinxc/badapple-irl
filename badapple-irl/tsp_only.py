import sys
import time
import numpy as np
import cv2
import numpy as np
from pathlib import Path
# add current directory to path
import sys
sys.path.append("~/src/badapple/badapple-irl/")
from python_tsp2.exact import solve_tsp_dynamic_programming


# setup
badapple_path = Path(".").resolve().parent / "badapple-small.mp4"
square_side = 30
# skip to frame 364 because I already did every frame before that
frame_start = 365

# get all the points in each frame
cap = cv2.VideoCapture(str(badapple_path))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"width: {width}, height: {height}, fps: {fps}, n_frames: {n_frames}")
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_start)

frame_count = 0
frame_points = []
original_frame_id_map = {}

print("Calculating dark areas of frames")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if frame_count % 100 == 0:
        print(f"frame {frame_count}/{(n_frames-frame_start)//2}", end="\r")
    frame_count += 1

    current_frame_pixels = set()
    for i in range(0, width - 1, square_side):
        for j in range(0, height - 1, square_side):
            section = frame[j: j + square_side, i: i + square_side]
            if (np.mean(section)) < 50:
                current_frame_pixels.add((i, j))
    frame_points.append(current_frame_pixels)
    original_frame_id_map[len(frame_points) - 1] = frame_start + (frame_count-1) * 2  # trust
    # skip a frame because I don't want to do every frame
    ret, frame = cap.read()
num_frames = len(frame_points)
print(f"\nnum_frames: {num_frames}")

# remove first 1000 frames from permutation.txt
with open("permutation.txt", "r") as f:
    permutation = [int(x.strip()) for x in f.readlines()]

perm_set = set(permutation[:1000])
frame_points_2 = []
original_id = {}
frames_done = []
for i in range(num_frames):
    if i in perm_set:
        continue
    else:
        original_id[len(frame_points_2)] = i
        frame_points_2.append(frame_points[i])
        frames_done.append(i)

print("Original ids")
print(original_id)
num_frames = len(frame_points_2)
# calculate the cost between every two frames (distance matrix), and then run TSP algorithm to get optimized order of frames
print(f"Calculating costs for {frames_done}")
print(f"Should be mutually exclusive with {permutation[0:1000]}")
costs = np.zeros((num_frames, num_frames))
for i in range(num_frames):
    for j in range(num_frames):
        costs[i][j] = len(frame_points_2[i] ^ frame_points_2[j])
        costs[j][i] = costs[i][j]
print(costs)
sys.setrecursionlimit(100000)
start_time = time.time()
permutation, distance = solve_tsp_dynamic_programming(costs)
print(permutation)
print(f"Time taken: {time.time() - start_time}")
print("Distance: ", distance)
# save the permutation
with open("permutation1000onward.txt", "w") as f:
    f.write(",".join([str(i) for i in permutation]))

# generate diff frames by comparing current frame with previous frame's set, making green for additions and red for removals

print("Generating frames")
last_frame_pixels = set()
for index in range(num_frames - 1):

    out_frame = np.ones((height, width, 3), dtype=np.uint8) * 255
    current_frame_pixels = frame_points_2[permutation[index]]

    for i in range(0, width - 1, square_side):
        for j in range(0, height - 1, square_side):
            if (i, j) in current_frame_pixels and (i, j) in last_frame_pixels:
                # persisted from previous frame. Black circle, white text
                circle_colour = (0, 0, 0)
                text_color = (255, 255, 255)
            elif (i, j) in current_frame_pixels:
                # new black dot. Green circle, black text
                circle_colour = (0, 255, 0)
                text_color = (0, 0, 0)
            elif (i, j) in last_frame_pixels:
                # removed black dot. Red circle, black text
                circle_colour = (0, 0, 255)
                text_color = (0, 0, 0)
            else:
                # persisted nothing. Just use black text
                text_color = (0, 0, 0)
                circle_colour = None
            if circle_colour is not None:
                cv2.circle(out_frame, (i + square_side // 2, j + square_side // 2), square_side // 2, circle_colour, -1)
            cv2.putText(out_frame, f"{j // square_side + 1}", (i + square_side // 3 - 1, j + 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, text_color, 1, cv2.LINE_AA)
            cv2.putText(out_frame, f"{i // square_side + 1}", (i + square_side // 3 - 1, j + 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, text_color, 1, cv2.LINE_AA)

    cv2.imwrite(f"diff_frames_opt_1000/{index}.png", out_frame)

    last_frame_pixels = current_frame_pixels