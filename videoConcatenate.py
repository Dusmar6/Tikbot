# -*- coding: utf-8 -*-
"""
https://zulko.github.io/moviepy/install.html
installed through that link, i did not use pip install or conda install because
it autoupdated something and created a problem, so i just downloaded and
installed the package manually using python install
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("video1.mp4")
clip2 = VideoFileClip("video2.mp4")

final_clip = concatenate_videoclips([clip1,clip2])
final_clip.write_videofile("my_concatenation.mp4")