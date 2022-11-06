Originally, I implemented an image hashing algorithm and then made a dict
with the key being the image and the value being the index of the closest frame.

This cache didn't trigger that often because the frames are pretty different.

Instead, I decided to speed up computation with multiprocessing, deleting the cache
since it might not do well in multiprocessing.