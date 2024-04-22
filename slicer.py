from moviepy.editor import VideoFileClip, VideoClip
import numpy as np
import os
import math
from PIL import Image

def slice_and_save_frames(video_path, start_time, end_time, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    clip = VideoFileClip(video_path)
    
    sliced_clip = clip.subclip(start_time, end_time)
    
    duration = sliced_clip.duration
    
    fps = sliced_clip.fps
    num_frames = int(duration * fps)

    frames = []
    
    for i in range(num_frames):
        frame_time = start_time + i / fps
        image_path = os.path.join(output_dir, f"frame_{i:04d}.png")
        sliced_clip.save_frame(image_path, t=frame_time)
        frame = Image.open(image_path)
        frames.append(frame)
    
    print(f"Saved {num_frames} frames to {output_dir}")
    return frames

def glue_frames_into_grid(frames, output_path):
    total_frames = len(frames)
    
    # Calculate grid dimensions nxn
    initial_size = math.floor(math.sqrt(total_frames))
    
    # Adjust the grid size if necessary
    grid_size = (initial_size, initial_size)
    while grid_size[0] * grid_size[1] < total_frames:
        grid_size = (grid_size[0] + 1, grid_size[1])
        if grid_size[0] * grid_size[1] < total_frames:
            grid_size = (grid_size[0], grid_size[1] + 1)
    
    frame_width = frames[0].width
    frame_height = frames[0].height
    
    grid_width = frame_width * grid_size[0]
    grid_height = frame_height * grid_size[1]
    
    grid_image = Image.new('RGB', (grid_width, grid_height))
    
    # Place each frame into the grid
    for i in range(total_frames):
        row = i // grid_size[0]
        col = i % grid_size[0]
        x = col * frame_width
        y = row * frame_height
        grid_image.paste(frames[i], (x, y))
    
    grid_image.save(output_path)
    print(f"Saved grid image to {output_path}")

def frames_to_gif(frames, output_path, fps=60):
    def make_frame(t):
        frame_index = int(t * fps)
        if frame_index < len(frames):
            frame = np.array(frames[frame_index])
            return frame
        else:
            return np.array(frames[-1])
    
    clip = VideoClip(make_frame, duration=len(frames)/fps)
    clip.write_gif(output_path, fps=fps)
    
    print(f"Saved GIF to {output_path}")


start_time = float(input("Enter start time (seconds): "))
end_time = float(input("Enter end time (seconds): "))

print("Enter file format:\nw - .webm\nm - .mp.4\ng - .gif")
user_input = str(input())
if user_input == 'w' or user_input == 'W':
    video_path = "./video.webm"
elif user_input == 'm' or user_input == 'M':
    video_path = "./video.mp4"
elif user_input == 'g' or user_input == 'G':
    video_path = "./video.gif"
else:
    print("Wrong input")
    exit()
print("Proceeding...")

output_dir = "./output"
output_image_path = "./grid_image.png"
output_gif_path = "./output_video.gif"

frames = slice_and_save_frames(video_path, start_time, end_time, output_dir)
glue_frames_into_grid(frames, output_image_path)
frames_to_gif(frames, output_gif_path)
