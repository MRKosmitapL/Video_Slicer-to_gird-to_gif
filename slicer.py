import fileinput
import os
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import customtkinter  # <- import the CustomTkinter module
#from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageTk

from moviepy.editor import VideoFileClip, VideoClip, ImageClip
import math
from PIL import Image
import numpy as np

root = tk.Tk()  # create the Tk window like you normally do
root.geometry("500x650")
root.minsize(500, 550)
root.resizable(width=False, height=False)
root.title("V1dE0 Slicer")


SpriteSheetFormat = ".png"
video_path = "empty"  # Imported file path
output_dir = "./output"
output_image_path = "./Grid"
output_gif_path = "./GIF.gif"
preview_path = "./preview"
input_dir = "./input"
frames = []
clip = None
#TO DO: 
#Load sprites from folder to make spritesheet and gif - DONE
#Input safety
#Progress Bar?
#Start and End time video preview??
#Option to Check frames for duplicates???
#Make spritesheets and gifs out of certain files in the folder (n,n+1,n+2..n+x).png????

# Current Troubles:
# Video length 60. Inputs: 43 - 44. FIXED
# OSError: MoviePy error: failed to read the first frame of video file video.mp4.
# you are using a deprecated version of FFMPEG. On Ubuntu/Debian for instance the version 
# in the repos is deprecated. Please update to a recent version from the website.
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
    
    if (total_frames == 0):
        logbox.insert(tk.CURRENT, f"No frames to make a spritesheet in {input_dir}"+"\n")
        return
    
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
    logbox.insert(tk.CURRENT, f"Saved grid image to {output_image_path}"+"\n")
    
def slice_and_save_frames():
    global frames
    global clip
    frames.clear()
    try:
        start_time = float(editStartTime.get()) #(seconds)
        end_time = float(editEndTime.get()) #(seconds)
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
    
    duration = end_time - start_time
    fps = clip.fps
    num_frames = int(duration * fps)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    for i in range(num_frames):
        frame_time = start_time + i/fps
        image_path = os.path.join(output_dir, f"frame_{i:04d}.jpg")
        clip.save_frame(image_path, t=frame_time)
        frame = Image.open(image_path)
        frames.append(frame)
    
    logbox.insert(tk.CURRENT, f"Saved {num_frames} frames to {output_dir}"+"\n")

def glue_frames_into_grid():
    
    global frames
    global output_image_path
    total_frames = len(frames)
    
    if (total_frames == 0):
        logbox.insert(tk.CURRENT, f"No sliced frames to make a spritsheet with\n")
        return
    
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
    
    print(x, y)
    print("------------------------------")
    
    grid_image.save(output_image_path+f"_{int(grid_image.width/frame_width)}_{int(grid_image.height/frame_height)}_{total_frames}"+SpriteSheetFormat)
    logbox.insert(tk.CURRENT, f"Saved grid image to {output_image_path}"+"\n")
    
def frames_to_gif(fps=60):
    global frames
    if (len(frames) == 0):
        logbox.insert(tk.CURRENT, f"No sliced frames to make a gif with\n")
        return
    
    #def make_frame(t):
    #    frame_index = int(t * fps)
    #    if frame_index < len(frames):
    #        frame = np.array(frames[frame_index])
    #        return frame
    #    else:
    #        return np.array(frames[-1])
    
    #clipGif = VideoClip(make_frame, duration=len(frames)/fps)
    #clipGif.write_gif(output_gif_path, fps=fps)
    first_frame = frames[0]
    first_frame.save(fp=output_gif_path, format='GIF', append_images=frames, save_all=True, duration=1, loop=0)
        
    logbox.insert(tk.CURRENT, f"Saved GIF to {output_gif_path}"+"\n")

#//////////////////////////////////////////////////////////////////////////// BUTTONS
def loadVideo():
    global video_path
    global frames
    global clip
    frames.clear()
    video_path = filedialog.askopenfilename(
        title="Select Video", filetypes=[("Videos", ".webm .mp4 .gif")]
    )
    if not video_path:
        labelFile.configure(text="Video not chosen")
    else:
        labelFile.configure(text=os.path.basename(video_path).split("/")[-1])
        buttonSliceAndSave.configure(state = "normal")
        
    try:
        clip = VideoFileClip(video_path)
    except:
        logbox.insert(tk.CURRENT, "Incorrect Video Path"+"\n")
        return  
    
    logbox.insert(tk.CURRENT, "Loaded video =" + video_path+"\n")
    
def create_preview():
    global frames
    global SpriteSheetFormat
    maxsize = (250,220)
    if not os.path.exists(preview_path):
        os.makedirs(preview_path)
    if not os.path.exists(preview_path+"/start"+SpriteSheetFormat):
            image = Image.new(mode="RGB", size=maxsize)
            if frames != None:
                image.paste(frames[0].resize(maxsize))
            image.save(preview_path+"/start"+SpriteSheetFormat)
    if not os.path.exists(preview_path+"/end"+SpriteSheetFormat):
        image = Image.new(mode="RGB", size=maxsize)
        image.save(preview_path+"/end"+SpriteSheetFormat)
        
    if frames != None:
        #Override first image
        image = Image.open(preview_path+"/start"+SpriteSheetFormat)
        image.paste(frames[0].resize(maxsize))
        image.save(preview_path+"/start"+SpriteSheetFormat)
        #Override second image
        image = Image.open(preview_path+"/end"+SpriteSheetFormat)
        image.paste(frames[-1].resize(maxsize))
        image.save(preview_path+"/end"+SpriteSheetFormat)
        
    #Override images
    previewImageStart.configure(light_image=Image.open(preview_path+"/start"+SpriteSheetFormat))
    previewImageEnd.configure(light_image=Image.open(preview_path+"/end"+SpriteSheetFormat))

    previewStartLabel.image = previewImageStart
    previewEndLabel.image = previewImageEnd
    
def get_radio_value():
    global SpriteSheetFormat
    global output_image_path
    SpriteSheetFormat = formatVar.get()
    output_image_path = "./Grid"+SpriteSheetFormat
    print(SpriteSheetFormat, output_image_path)
    
# Use CTkButton instead of tkinter Button
#//////////////////////////////////////////////////////////////////////////// INTERFACE
#Fonts
thickFont=customtkinter.CTkFont('Arial', 16)
# BUTTONS
buttonUpload = customtkinter.CTkButton(
    master=root, text="Load video", corner_radius=5, command=loadVideo, font = thickFont
)
buttonUpload.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
# 
buttonSliceAndSave = customtkinter.CTkButton(
    master=root, text="Slice Frames", corner_radius=5, command=slice_and_save_frames, font = thickFont
)
buttonSliceAndSave.place(relx=0.5, y=35, rely=0.5, anchor=tk.CENTER)
# 
createPreview = customtkinter.CTkButton(
    master=root, text="See Preview", corner_radius=5, command=create_preview, font = thickFont
)
createPreview.place(relx=0.5, y=70, rely=0.5, anchor=tk.CENTER)
#
makeGrid = customtkinter.CTkButton(
    master=root, text="Make Spritesheet", corner_radius=5, command=glue_frames_into_grid, font = thickFont
)
makeGrid.place(x = 80, y=105, rely=0.5, anchor=tk.CENTER)
#
makeGif = customtkinter.CTkButton(
    master=root, text="Make Gif", corner_radius=5, command=frames_to_gif, font = thickFont
)
makeGif.place(x=-80, relx=1, y=105, rely=0.5, anchor=tk.CENTER)
#
buttonGridFromFolder = customtkinter.CTkButton(
    master=root, text="Spritesheet from folder", corner_radius=5, command=glue_frames_into_grid_from_folder, font = thickFont
)
buttonGridFromFolder.place(relx=0.5, y=105, rely=0.5, anchor=tk.CENTER)
# Edits
editStartTime = customtkinter.CTkEntry(master=root, width=60, height=25, corner_radius=5)
editStartTime.place(relx=0.15, rely=0.5, anchor=tk.CENTER)
editStartTime.insert(0, "0")
#
editEndTime = customtkinter.CTkEntry(master=root, width=60, height=25, corner_radius=5)
editEndTime.place(relx=0.85, rely=0.5, anchor=tk.CENTER)
editEndTime.insert(0, "1")
# JUST LABELS
labelFile = customtkinter.CTkLabel(master=root, text="No uploaded video")
labelFile.place(relx=0.5, y=20, anchor=tk.CENTER)
labelStartTime = customtkinter.CTkLabel(master=root, text="Start time")
labelStartTime.place(relx=0.15,y=30, rely=0.5, anchor=tk.CENTER)
labelEndTime = customtkinter.CTkLabel(master=root, text="End time")
labelEndTime.place(relx=0.85,y=30, rely=0.5, anchor=tk.CENTER)

#RadioButtons to choose spritesheet format png/jpg
formatLabel = customtkinter.CTkLabel(root, text="Select Spritesheet format", bg_color="#3B8ED0", text_color="#ffffff", corner_radius=10, font=thickFont)
formatLabel.place(relx=0.215, y=30, rely=0.68, anchor=tk.CENTER)
formatVar = customtkinter.StringVar(value=".png")
#png
formatRad1 = customtkinter.CTkRadioButton(root, text=".png", value=".png", variable=formatVar, command=get_radio_value, bg_color="#3B8ED0", text_color="#ffffff",fg_color="#ffffff", radiobutton_height=12, radiobutton_width=12, width=50, height=25)
formatRad1.place(relx=0.5,y=30, rely=0.68, anchor=tk.CENTER)
#jpg
formatRad2 = customtkinter.CTkRadioButton(root, text=".jpg", value=".jpg", variable=formatVar, command=get_radio_value, bg_color="#3B8ED0", text_color="#ffffff",fg_color="#ffffff", radiobutton_height=12, radiobutton_width=12, width=50, height=25)
formatRad2.place(relx=0.65,y=30, rely=0.68, anchor=tk.CENTER)

# TextBox for Logs
logbox = customtkinter.CTkTextbox(master = root, width = 500, height = 150)
logbox.place(relx=0.5, rely=0.87, anchor=tk.CENTER)

# Preview
previewImageStart = customtkinter.CTkImage(light_image=Image.new(mode="RGB", size=(250, 220)),
                                    size=(250, 220))
previewImageEnd = customtkinter.CTkImage(light_image=Image.new(mode="RGB", size=(250, 220)),
                                size=(250, 220))

previewStartLabel = customtkinter.CTkLabel(master=root, image=previewImageStart, text="") 
previewStartLabel.place(x=125, rely=0.25, anchor=tk.CENTER)
previewEndLabel = customtkinter.CTkLabel(master=root, image=previewImageEnd, text="") 
previewEndLabel.place(x=-125,relx=1, rely=0.25, anchor=tk.CENTER)
#//////////////////////////////////////////////////////////////////////////// MAIN

root.mainloop()
