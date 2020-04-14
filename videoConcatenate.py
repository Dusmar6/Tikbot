# -*- coding: utf-8 -*-

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def concatenate_clips(folder, name, clip_paths):
    
    final_clip = concatenate_videoclips(clip_paths)
    final_clip.write_videofile(os.path.join(folder, name + ".mp4"))