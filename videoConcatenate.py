# -*- coding: utf-8 -*-


import os
import glob





def concatenate_clips(folder, name, clip_paths, temp_folder):
    
    print(os.path.join(clip_paths,"*.mp4"))
    stringa = "ffmpeg -i \"concat:"
    elenco_video = glob.glob(os.path.join(clip_paths,"*.mp4"))
    
    print(elenco_video)
    elenco_file_temp = []
    for f in elenco_video:
        file = os.path.join(temp_folder, "temp" + str(elenco_video.index(f) + 1) + ".ts")
        os.system("ffmpeg -i " + f + " -c copy -bsf:v h264_mp4toannexb -f mpegts " + file)
        elenco_file_temp.append(file)

    for f in elenco_file_temp:
        stringa += f
        if elenco_file_temp.index(f) != len(elenco_file_temp)-1:
            stringa += "|"
        else:
            stringa += "\" -c copy  -bsf:a aac_adtstoasc " + os.path.join(folder, name) + ".mp4"

    os.system(stringa)
    
    files = glob.glob(os.path.join(temp_folder, '*'))
    for f in files:
        os.remove(f)
    