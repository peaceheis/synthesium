import os
import os.path
import shutil
import tempfile
from typing import Iterable

import ffmpeg
from cairo import ImageSurface
import cairo

from synthesium.utils.imports import *
from synthesium.matables.primitives import Line, Arc, Curve
from synthesium.matables.matable import Matable
from synthesium.matables.matablegroup import MatableGroup
from synthesium.mations.mations import ConcurrentMation, Mation



class Canvas(): 
    def __init__(self, /, background_color=(0, 0, 0, 1), fps=24, frame_size=(2000, 1600)): #TODO, make a better default frame size
        self.mations = []
        self.background_color = background_color
        self.fps = fps
        self.width = frame_size[0]
        self.height = frame_size[1]

        #cairo things
        self.surface = ImageSurface(cairo.Format.ARGB32, self.width, self.height)
        self.bg_ctx = cairo.Context(self.surface)
        self.initialize_surface()
    
        
    def initialize_surface(self): 
        #initialize background color
        self.ctx.move_to(0, 0)
        self.ctx.set_source_rgba(*self.background_color[:3], self.background_color[3])
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()


    def add_mation(self, *mations): 
        """calling self.add(mation) doesn't do much besides add it to the list of Mations to be processed. The heavy lifting is done when
        Canvas.view() is called, outside the class definition."""
        for mation in mations: 
            mation.set_fps(self.fps)
            self.mations.append(mation)

    def save(self, tmpdir: str, enddir: str): 
        """This is where all the rendering work gets done. First, the mationlist is sorted by end frame,
        then the """
        #sort list of Mations
        sorter = lambda mation: mation.get_start_frame()
        mationlist: list[Matable] = sorted(self.mations, key=sorter)

        total_frames = mationlist[-1].get_end_frame(self.fps)
        import time


        os.chdir(tmpdir)

        time.sleep(2)
        for i in range(total_frames): 
            active_mations = [mation for mation in mationlist if i in mation.get_range_of_frames()]
            for mation in active_mations: self.surface = mation.tick().draw(self.surface, self.ctx)

            #write
            if i < 10:
                self.surface.write_to_png("{}/00{}temp.png".format(tmpdir, i))
            elif i < 100:
                self.surface.write_to_png("{}/0{}temp.png".format(tmpdir, i)) #TODO, convert to adding an ffmpeg pipe with np array, MUCH easier on disk and much faster.
            else: 
                self.surface.write_to_png("{}/{}temp.png".format(tmpdir, i))
            self.initialize_surface()

        #finish
        cmd = "ffmpeg -framerate "
        cmd += str(self.fps)
        cmd += " -i "
        cmd += tmpdir
        cmd += "/"
        cmd += "%03dtemp.png -vcodec mpeg4 " 
        cmd += enddir
        os.system(cmd)
        print(cmd)

    def write(self, /, tmpdir: str, enddir: str): 
        self.construct()
        self.save(tmpdir, enddir)

    def construct(self): 
        """Construct() lies at the heart of Synthesium. All Mations should be played in self.construct(), which the 
        internal pipeline looks for when creating an animation. """
        
