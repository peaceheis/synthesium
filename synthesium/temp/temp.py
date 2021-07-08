import os

def write(surface, num):
    if num < 10:
        surface.write_to_png(f"path/to/folder/{num}temp.png")
    else: 
        surface.write_to_png(f"/path/to/folder{num}temp.png") #TODO, make better system

def finish(fps):
    os.system(f"ffmpeg -f image2 -r 24 -i path/to/folder/%dtemp.png -vcodec mpeg4 -y /path/to/finished.mp4")