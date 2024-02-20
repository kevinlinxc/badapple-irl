import cv2
import numpy as np

import sys
from timeit import default_timer as timer
import multiprocessing
import glob
import os


def progress(purpose, currentcount, maxcount):
    """Generic progress printout"""
    sys.stdout.write("\r")
    sys.stdout.write(
        "{}: {} of {}, {:.2f}%".format(
            purpose, currentcount + 1, maxcount, (currentcount + 1) / maxcount * 100
        )
    )
    sys.stdout.flush()


def phash(cv_image):
    """Hash algorithm for an image to detect duplicates"""
    h = cv2.img_hash.pHash(cv_image)  # 8-byte hash
    return int.from_bytes(h.tobytes(), byteorder="big", signed=False)


def downscale_video(video_path, scale_factor):
    """
    Downscales video and returns downscaled frames in a list.
    Also saves using numpy so this function only runs once per scale_factor
    """
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out = []
    known_hashes = set()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # convert to grayscale and downscale by scale_width
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(
            frame, (int(width / scale_factor), int(height / scale_factor))
        )

        frame_hash = phash(frame)
        # check if hash is in known_hashes
        if frame_hash not in known_hashes:
            out.append(frame)
            known_hashes.add(frame_hash)
        # progress printout
        if len(out) % 100 == 0 or len(out) == total_frames:
            progress("downscaling video", len(out), total_frames)
    cap.release()

    # save this output list of ndarrays, so we don't have to downscale the video after the first time
    print("\nSaving to {}split.npy".format(scale_factor))
    np.save(f"{scale_factor}split.npy", out)
    return out


def get_closest_frame(frame, frames):
    """Returns the closest frame in frames to the given frame"""
    return min(frames, key=lambda x: cv2.norm(frame, x, cv2.NORM_L2))


def multiprocess_frame_replacement(
    frame, frames, output_name, width, height, small_width, small_height
):
    """
    Bite-sized task to replace split x split sections in the video with the closest frames from frames.
    All cores are taking tasks from the list and running this function.
    """
    out_path = os.path.join("output", output_name)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out_frame = frame.copy()
    # break down frame into sections and replace with the closest frame from frames
    if (mean := np.mean(frame)) in [0, 255]:
        # white and black frames exist in the video, so just frames that are black or white are trivial
        print(f"{output_name} had mean of {mean}, skipping", flush=True)
        cv2.imwrite(out_path, out_frame)
        return
    for i in range(0, width - 1, small_width):
        for j in range(0, height - 1, small_height):
            # get section of frame
            section = frame[j : j + small_height, i : i + small_width]

            if (np.mean(section)) in [0, 255]:
                # again, if a subsection is all black or white then they are trivial, and we shouldn't
                # waste time looking for the closest frame
                continue

            # get closest frame
            closest_frame = get_closest_frame(section, frames)

            # replace section with the closest frame
            out_frame[j : j + small_height, i : i + small_width] = closest_frame
    print(f"writing {output_name}", flush=True)
    cv2.imwrite(out_path, out_frame)


def bad_apple(vid_path: str, frames, width, height, small_width, small_height):
    # setup function for the multiprocessing
    print(f"total unique downscaled frames: {len(frames)}")

    cap = cv2.VideoCapture(vid_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0

    pool_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # chunk the video into 500 frame chunks and run multiprocessing starmap on them
        # This chunking is just because I don't have enough ram to store all the jobs in memory
        if len(pool_list) == 500 or count == total_frames - 1:
            print("Pool full, processing these frames")
            with multiprocessing.Pool(4) as pool:
                pool.starmap(multiprocess_frame_replacement, pool_list)
            pool_list = []
        output_name = str(count) + ".png"
        out_path = os.path.join("output", output_name)

        # if out_path already exists, skip (for if I stop the script and restart it)
        if os.path.exists(out_path):
            print(f"Skipping {out_path}, exists already", flush=True)
        else:
            print(f"Adding {output_name} to work pool", flush=True)
            pool_list.append(
                (frame, frames, output_name, width, height, small_width, small_height)
            )
        count += 1
    cap.release()


def compile_video(width, height, fps):
    pictures_glob = os.path.join("output", "*.png")
    files = sorted(glob.glob(pictures_glob), key=len)

    print(files)
    # write files to mp4 using opencv
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))
    for index, file in enumerate(files):
        if index % 100 == 0 or index == len(files) - 1:
            progress("compiling video", index, len(files))
        frame = cv2.imread(file)
        out.write(frame)
    out.release()


if __name__ == "__main__":
    vid_path_ = "../badapple.mp4"
    split = 5  # amount to scale down the video to use as replacements for sections of the original video
    try:
        print(f"loading from {split}split.npy")
        frames_ = np.load(f"{split}split.npy")
    except FileNotFoundError:
        print(f"Downscaling video by {split}")
        frames_ = downscale_video(vid_path_, split)

    cap_ = cv2.VideoCapture(vid_path_)
    width_ = int(cap_.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_ = int(cap_.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_ = cap_.get(cv2.CAP_PROP_FPS)
    cap_.release()
    # get width and height of small frames
    small_height_, small_width_ = frames_[0].shape[:2]
    print(
        f"width: {width_}, height: {height_}, small_width: {small_width_}, small_height: {small_height_}"
    )

    start = timer()
    bad_apple("../badapple.mp4", frames_, width_, height_, small_width_, small_height_)
    end = timer()

    print(f"Time taken for finding nearest neighbours: {end - start}")

    compile_video(width_, height_, fps_)
