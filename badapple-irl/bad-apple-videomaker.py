import os
import cv2
import numpy as np

pre_tsp_frames_dir = r"K:\bad-apple-processed\pre-tsp"
tsp_frames = r"K:\bad-apple-processed\tsp"
pre_tsp_files = os.listdir(pre_tsp_frames_dir)
tsp_files = os.listdir(tsp_frames)

# make opencv video with 30fps, 960x720

# open one file for frame size
print(f"Total frames: pre-tsp: {len(pre_tsp_files)}, tsp: {len(tsp_files)}")
img = cv2.imread(os.path.join(pre_tsp_frames_dir, pre_tsp_files[0]))
height, width, layers = img.shape
print("Original shape: ", img.shape)
print("aaaa")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# scale
first_video = cv2.VideoWriter('pre-tsp-video.mp4', fourcc, 30, (width, height))
just_frame_number1 = cv2.VideoWriter("just_frame_number_pre-tsp1.mp4", fourcc, 30, (700, 100))
for index, file in enumerate(pre_tsp_files):
    blank_text_number = np.zeros((100, 700, 3), np.uint8)
    blank_text_number = cv2.putText(blank_text_number, f"{file}", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 255, 255), 2, cv2.LINE_AA)
    just_frame_number1.write(blank_text_number)
#     img = cv2.imread(os.path.join(pre_tsp_frames_dir, file))
#     # some frames have the wrong size, resize to the correct width and height
#     img = cv2.resize(img, (width, height))
#     print(f"first video progress: {index}/364, file: {file}", flush=True)
#     first_video.write(img)
#
# first_video.release()

# make second video by reversing the permutation from permutation.txt

permutation = [int(x.strip()) for x in open("permutation.txt", "r").readlines()]
# revert from frame order to tsp solution order (frame 365, frame 367, frame 369) to (frame 0, frame 1, frame 2)
permutation = [(x-365)//2 for x in permutation]
# create a dictionary so we know where to look for frame i
# if we want frame 2, we want image 3104 because frame 2 is last in the permutation. So, we lookup permutation[i]
# and get i
permutation_lookup = {permutation[i] : i for i in range(len(permutation))}

# 15 fps for this video since I cut framerate in half.

img = cv2.imread(os.path.join(tsp_frames, tsp_files[0]))
height, width, layers = img.shape
print("Original shape: ", img.shape)
print("aaaa")
# second_video = cv2.VideoWriter('tsp-video-final2.mp4', fourcc, 15, (width, height))
just_frame_number2 = cv2.VideoWriter("just_frame_number_tsp.mp4", fourcc, 15, (700, 100))

for i in range(len(tsp_files)):
    file_name = tsp_files[permutation_lookup[i]]
    # img = cv2.imread(os.path.join(tsp_frames, file_name))
    # img = cv2.resize(img, (width, height))
    if "Copy" in file_name:
        file_name = file_name.replace(" - Copy", "") # i named frames copy when I had to insert a frame
        # but it's probably less jarring for the viewer if they don't have to see that
    # put the file name on the text so I can find defects
    blank_text_number = np.zeros((100, 700, 3), np.uint8)
    blank_text_number = cv2.putText(blank_text_number, f"{file_name}", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    just_frame_number2.write(blank_text_number)
    # cv2.imshow("with text", img)
    # cv2.waitKey(0)
    print(f"second video progress: {i}/3104, file: {tsp_files[permutation_lookup[i]]}", flush=True)
    # second_video.write(img)

first_video.release()
just_frame_number1.release()
just_frame_number2.release()
# second_video.release()
