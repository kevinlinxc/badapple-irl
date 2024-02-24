# replace_subframes_with_frames
This was an old idea I had of replacing portions of Bad Apple frames with other downscaled
Bad Apple frames. My methodology for finding similarity between 
frames (OpenCV Norm brute forcing) was very slow, and it took over 4 days to process.

If I had to do it again, I would use https://github.com/dermotte/liresolr, which
is a pre-built solution for finding image similarity. Someone else did it this way, and it was wayyy faster.