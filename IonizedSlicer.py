import fileinput
import os
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import customtkinter  # <- import the CustomTkinter module
#from tkVideoPlayer import TkinterVideo





from moviepy.editor import VideoFileClip, VideoClip, ImageClip
import math
from PIL import Image
import numpy as np

root = tk.Tk()  # create the Tk window like you normally do
root.geometry("400x550")
root.minsize(400, 550)
root.resizable(width=False, height=False)
root.title("V1dE0 Slicer")

video_path = "empty"  # Imported file path
output_dir = "./output"
output_image_path = "./Grid.png"
output_gif_path = "./GIF.gif"
input_dir = "./input"
frames = []
#TO DO: 
#Load sprites from folder to make spritesheet and gif - DONE
#Input safety
#Progress Bar?
#Start and End time video preview??
#Option to Check frames for duplicates???
#Make spritesheets and gifs out of certain files in the folder (n,n+1,n+2..n+x).png????
#//////////////////////////////////////////////////////////////////////////// SLICER
def glue_frames_into_grid_from_folder():
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    
    global frames
    frames.clear()
    frame_path = os.listdir(input_dir)
    for frame in frame_path:
        frame = Image.open(input_dir+"/"+frame)
        frames.append(frame)

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
    
    grid_image.save(output_image_path)
    #print(f"Saved grid image to {output_image_path}")
    logbox.insert(tk.CURRENT, f"Saved grid image to {output_image_path}"+"\n")
    
def slice_and_save_frames():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        start_time = float(editStartTime.get()) #start time (seconds)
        end_time = float(editEndTime.get()) #end time (seconds)
    except:
        logbox.insert(tk.CURRENT, "Incorrect Time Input"+"\n")
        return
    
    if (start_time == end_time):
        logbox.insert(tk.CURRENT, "Start time = end time. Zero frames"+"\n")
        return
    
    if (start_time > end_time):
        z = start_time
        start_time = end_time
        end_time = z
        
    
    clip = VideoFileClip(video_path)
    
    sliced_clip = clip.subclip(start_time, end_time)
    
    duration = sliced_clip.duration
    
    fps = sliced_clip.fps
    num_frames = int(duration * fps)

    global frames
    
    for i in range(num_frames):
        frame_time = start_time + i / fps
        image_path = os.path.join(output_dir, f"frame_{i:04d}.png")
        sliced_clip.save_frame(image_path, t=frame_time)
        frame = Image.open(image_path)
        frames.append(frame)
    
    #print(f"Saved {num_frames} frames to {output_dir}")
    logbox.insert(tk.CURRENT, f"Saved {num_frames} frames to {output_dir}"+"\n")

def glue_frames_into_grid():
    global frames
    global output_image_path
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
    
    grid_image.save(output_image_path)
    #print(f"Saved grid image to {output_image_path}")
    logbox.insert(tk.CURRENT, f"Saved grid image to {output_image_path}"+"\n")
    
def frames_to_gif(fps=60):
    global frames
    
    def make_frame(t):
        frame_index = int(t * fps)
        if frame_index < len(frames):
            frame = np.array(frames[frame_index])
            return frame
        else:
            return np.array(frames[-1])
    
    clip = VideoClip(make_frame, duration=len(frames)/fps)
    clip.write_gif(output_gif_path, fps=fps)
    
    #print(f"Saved GIF to {output_path}")
    logbox.insert(tk.CURRENT, f"Saved GIF to {output_gif_path}"+"\n")

#//////////////////////////////////////////////////////////////////////////// BUTTONS
def loadVideo():
    global video_path
    video_path = filedialog.askopenfilename(
        title="Select Video", filetypes=[("Videos", ".webm .mp4 .gif")]
    )
    if not video_path:
        labelFile.configure(text="Video not chosen")
    else:
        labelFile.configure(text=os.path.basename(video_path).split("/")[-1])
        buttonSliceAndSave.configure(state = "normal")
    #print("Loaded video =" + video_path)
    try:
        start_time = float(editStartTime.get()) #start time (seconds)
        end_time = float(editEndTime.get()) #end time (seconds)
    except:
        logbox.insert(tk.CURRENT, "Incorrect Time Input"+"\n")
        return
    #///////////////////////////// I don't have enough time to implement this today so here's a plan of what i wanted to do
    #1. Make a slicedImageCLip
    #2. crate temp folder and saved it there (tkVideoPlayer probably doesn't allow to play videos from objects so we have to save it and take it's path)
    #3. Play preview in this windows (or separated idk)
    #4. When program closes delete temp folder and temp video
    # But the sliced .gif - .mp4 conversion doesn't work, it returns correct duration of video but the content is missing
    
    #if not os.path.exists("./tempdir"):
    #    os.makedirs("./tempdir")
        
    #clip = ImageClip(video_path)
    #sliced_clip = clip.subclip(start_time, end_time)
    #sliced_clip.set_duration(end_time-start_time)
    #sliced_clip.write_videofile("movie.mp4", fps=24, codec='mpeg4')
    #video_player = TkinterVideo(master=root, scaled=True)
    #video_player.load(sliced_clip)
    #video_player.pack(expand=True, fill="both")
    #video_player.play()
    #player = tkvideo(sliced_clip,"test", loop = 1, size = (1280,720))
    #player.play()
   #print(sliced_clip)
    
    logbox.insert(tk.CURRENT, "Loaded video =" + video_path+"\n")

# Use CTkButton instead of tkinter Button
#//////////////////////////////////////////////////////////////////////////// INTERFACE
# BUTTONS
buttonUpload = customtkinter.CTkButton(
    master=root, text="Load video", corner_radius=10, command=loadVideo
)
buttonUpload.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
# 
buttonSliceAndSave = customtkinter.CTkButton(
    master=root, text="Slice the Frames", corner_radius=10, command=slice_and_save_frames, state = "enabled"
)
buttonSliceAndSave.place(relx=0.5, y=35, rely=0.5, anchor=tk.CENTER)
#
makeGrid = customtkinter.CTkButton(
    master=root, text="Create Spritesheet", corner_radius=10, command=glue_frames_into_grid
)
makeGrid.place(relx=0.25, y=70, rely=0.5, anchor=tk.CENTER)
#
makeGif = customtkinter.CTkButton(
    master=root, text="Create Gif", corner_radius=10, command=frames_to_gif
)
makeGif.place(relx=0.75, y=70, rely=0.5, anchor=tk.CENTER)
#
buttonGridFromFolder = customtkinter.CTkButton(
    master=root, text="Create Spritesheet from folder", corner_radius=10, command=glue_frames_into_grid_from_folder
)
buttonGridFromFolder.place(relx=0.5, y=105, rely=0.5, anchor=tk.CENTER)
# Edits
editStartTime = customtkinter.CTkEntry(master=root, width=60, height=25, corner_radius=10)
editStartTime.place(relx=0.15, rely=0.5, anchor=tk.CENTER)
editStartTime.insert(0, "0")
#
editEndTime = customtkinter.CTkEntry(master=root, width=60, height=25, corner_radius=10)
editEndTime.place(relx=0.85, rely=0.5, anchor=tk.CENTER)
editEndTime.insert(0, "1")
# JUST LABELS
labelFile = customtkinter.CTkLabel(master=root, text="No uploaded video")
labelFile.place(relx=0.5, y=30, anchor=tk.CENTER)
labelStartTime = customtkinter.CTkLabel(master=root, text="Start time")
labelStartTime.place(relx=0.15,y=30, rely=0.5, anchor=tk.CENTER)
labelEndTime = customtkinter.CTkLabel(master=root, text="End time")
labelEndTime.place(relx=0.85,y=30, rely=0.5, anchor=tk.CENTER)
# TextBox for Logs
logbox = customtkinter.CTkTextbox(master = root, width = 400, height = 125)
logbox.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

#//////////////////////////////////////////////////////////////////////////// MAIN

root.mainloop()
