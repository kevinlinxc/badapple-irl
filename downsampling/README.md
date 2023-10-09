# Downsampling

The idea behind this module is to downsample the Bad Apple!! video into circles, so that I
can recreate the video in real life using actual (fake) apples. 

## downsample-video.py
This script was helping me decide on a downsampling resolution.

The original video is 960x720, and I played around with different downsampling resolutions.
For example, I tried binning every 20x20 square into a black or white circle, and the
video was still pretty crisp, however, I would need 960x720/(20x20) = 1728 apples for this, which
is not only expensive, but would take a prohibitively long time to move.

I started scouting for apples, and found some decent looking ones on Aliexpress. These
were 3cm in diameter, and the surface I planned to use was around 78cm wide, meaning I could
 fit 26 apples in a row. I found that dividing the original video into 30x30 squares of pixels to make a resolution of 
32x24 would be a good compromise, and the 24 fits nicely into the 26 rows I could do. 
This means I would only need to buy 768 apples, which is much more reasonable.

## max-apple-moves.py
Before buying the apples, I wanted to make sure that I could complete this project in a reasonable
timespan. To do this, I needed to calculate how many times I would have to move apples.
To calculate the maximum number of moves, I tracked how many pixels changed from white to black or black to white
between frames. This was basically just an exclusive or operation between the two frames' sets.

Using this method, I found that I would need at most 147688 moves. Assuming each move would take 5 seconds,
this equated to 12307 minutes, or 205 hours, or 8.5 days. This was a bit too long for me, so I decided to see if
I could optimize the moves early.


## min-apple-moves.py
I minimized the moves by including the fact that you could move apples from a formerly black spot to
a new black spot, thus not double counting some moves. Mathematically, this just meant that the moves between two frames
was the maximum of the white-to-black transitions and the black-to-white transitions. This reduced the number moves
down to 96351, which was a decent size decrease. At this point, I realized that using cartesian
coordinates to try and coordinate moves was probably dumb, and that it would be much faster
to just create "diffs", where I have an image that has additions in green and removals in red. This would
allow me to quickly memorize a few moves and remove them. Assuming that each move instead takes 1 second using this 
method, this gives 1605 minutes, 26.5 hours, or just over a day. This is totally feasible!
