# Video_Slicer-to_gird/to_gif
Supports .webm/.mp4/.gif files
---
# Installing
1. Make a new folder (for example movieSlicer)
2. Download slider.py and place it in "movieSlicer" folder
3. make sure you have moviepy, numpy, pillow installed
```
pip install moviepy==2.0.0.dev2 (or newer)
pip install Pillow
pip install numpy
```
---

# Using

1. Put a video file of your likings inside the folder where slicer.py is located
2. ***Rename video file to "video.mp4/.webm/.gif"***
3. Open terminal/console
4. Go to the same folder where slicer.py is located
5. run "python .\slicer.py"
6. Input start_time and end_time in seconds (can be with decimal places)
7. ***Don't worry about "File not found" message, I don't know why it shows up***
8. Input video file format
9. Wait until the process is finished, it may appear as it's stuck but it's not
10. There should be created a folder called "output" where all frames are saved, outside the folder "grid_image.png" and "output_video.gif" should be created
11. >profit

## There's no user input failstates implemented yet so if something doesn't seem right just press ctrl + c
