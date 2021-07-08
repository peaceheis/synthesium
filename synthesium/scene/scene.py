from synthesium.temp import temp
from synthesium.utils.useful_functions import linear_increase
from typing import Iterable
import os, os.path

from cairo import ImageSurface
import ffmpeg

from ..utils.imports import *
from ..matables.matables import Matable, Circle, Line
from ..mations.mations import Mation, ConcurrentMation, Move
from ..temp import temp

class Scene(): 
    def __init__(self, *, background_color=(0, 0, 0, 1), fps=24, frame_size=(1028, 1028)): #TODO, make a better default frame size
        self.mations = []
        self.background_color = background_color
        self.fps = fps
        self.width = frame_size[0]
        self.height = frame_size[1]

        #cairo things
        self.surface = ImageSurface(cairo.Format.ARGB32, self.width, self.height)
        self.ctx = cairo.Context(self.surface)
        self.arr = np.ndarray(shape=(self.height, self.width), dtype=np.uint32)
    
        
    def initialize_surface(self): 
        #initialize background color
        self.ctx.move_to(0, 0)
        self.ctx.set_source_rgba(*self.background_color[:3], self.background_color[3])
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()
        f = open("/Users/scakolatse/thing.png", "w")
        self.surface.write_to_png("/Users/scakolatse/thing.png")

    def play(self, *mations): 
        """calling self.add(mation) doesn't do much besides add it to the list of Mations to be processed. The heavy lifting is done when
        Scene.view() is called, outside the class definition."""
        for mation in mations: 
            mation.set_fps(self.fps)
            self.mations.append(mation)

        

    def save(self): 
        #sort list of Mations
        sorter = lambda mation: mation.get_start_frame()
        mationlist: list[Matable] = sorted(self.mations, key=sorter)

        total_frames = mationlist[-1].get_end_frame(self.fps)
        print(total_frames)
        import time
        time.sleep(2)

        for i in range(total_frames): 
            active_mations = [mation for mation in mationlist if i in mation.get_range_of_frames()]
            for mation in active_mations: self.surface = mation.tick().draw(self.surface, self.ctx)
            temp.write(self.surface, i)
            self.initialize_surface()

        temp.finish(self.fps)




    def construct(self): 
        """Construct() lies at the heart of Synthesium. All Mations should be played in self.construct(), which the 
        internal pipeline looks for when creating an animation. """
        



            
