import os
import os.path
from synthesium.utils.defaults import DEFAULT_FPS, FFMPEG_BIN
import subprocess

import numpy
from cairo import ImageSurface
import cairo

from synthesium.utils.imports import *
from synthesium.matables.primitives import * #Line, Arc, Curve
from synthesium.matables.matable import Matable
from synthesium.matables.matablegroup import MatableGroup
from synthesium.mations.mation import Mation
from synthesium.mations.mationgroup import MationGroup

class Canvas():  
    """The canvas acts as the entry point between the user and Synthesium. The user creates a class that inherits from Canvas,
       overrides construct, and then instantiates their custom class, then runs save("end_directory"), which returns the 
       finished video. All the rendering goes on in here, breaking MatableGroups down to Primitives, and then cairo draws the 
       primitives. In addition, animation goes on here, by calling tick on every active Mation."""

    def __init__(self, /, background_color=(0, 0, 0, 1), fps=DEFAULT_FPS, frame_size=(2000, 1600)): #TODO, make a better default frame size
        self.mations = []
        self.background_color = background_color
        self.fps = fps
        self.width = frame_size[0]
        self.height = frame_size[1]

        #cairo things
        self.surface = ImageSurface(cairo.Format.ARGB32, self.width, self.height)
        self.ctx = cairo.Context(self.surface)
        self.initialize_surface()
    
    def get_dimensions(self): 
        return (self.width, self.height)

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

    #auxiliary functiosn to save()

    def sort_mationlist(self):
        """Sorts the mationlist by start frame. It assumes that the animations have been play()ed, and therefore have
           had their fps set, because otherwise, how would they be in self.mations in the first place?"""
        
        return sorted(self.mations, key=Mation.get_start_frame())

    def merge_mations(self, mationlist):
        """Take all the mations in a list and compress them into a list of MationGroup to remove any overlap between 
           Mations. This is used with Canvas to ensure only one Mation (or MationGroup) has to be handled at a time."""
        merged_list = []
        len_minus_1 = len(mationlist) - 1 #it's used a lot, nice for convenience. 

        def overlap(mation1: Mation, mation2: Mation): 
            return mation1.get_end_frame() >= mation2.get_start_frame() #check if the second mation starts before or when the first mation ends.
        
        current_group = MationGroup() #initialize an empty MationGroup for mations to be added later.
        for i in range(len_minus_1): 
            mation1 = mationlist[i]
            mation2 = mationlist[i+1]

            if overlap(mation1, mation2): 
                current_group.add(mation1) #just the first one to avoid repetition, as mation2 will get added when i gets incremented.
            
            else:
                if len(current_group.get_mations()) > 0: #makes sure the MationGroup isn't empty, which would defeat the purpose of the group.
                    current_group.add(mation1)
                    merged_list += current_group
                
                else: 
                    merged_list += mation1 #if there's nothing in the MationGroup, just add the Mation by itself
        return merged_list

    def prepare_for_rendering(self, end_dir): 
        if not os.path.split()[0].exists(): 
            raise Exception(f"directory {end_dir} provided to Canvas {self.__class__.__name__} does not exist.")

        command = [
            FFMPEG_BIN, 
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', '{}, {}'.format(self.width, self.height),  # size of one frame
            '-pix_fmt', 'rgba',
            '-r', str(self.fps),  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
        ]  
        command += [
                '-vcodec', 'qtrle',
            ] #TODO hard coded transparency..... sub-optimal at best.
            
        command += [end_dir] #TODO, implement partial movie files à la Manim.
        return subprocess.Popen(command, stdin=subprocess.PIPE)
        #credit to Manim (github.com/3b1b/manim). I adapted this code from scene.file-writer.py, in the cairo-backend branch.

    def save(self, end_dir: str): 
        """This is where all the rendering work gets done. The steps are as follows:
                1. The mation list is sorted by start frame,
                2. A compressed list where any overlapping Mations are made into a MationGroup is generated,
                3. After verification of the end directory, a pipe is opened to ffmpeg to string together all the frames.
                Then things get interesting. 
                5. The animation gets rendered via loop: 
                    5a. Make the animation progress 1 frame.
                    5b. Get, and draw, all the Lines to be drawn.
                    5c. Get, and draw, all the Arcs to be drawn.
                    5d. Get, and draw, all the Curves to be drawn (5b - 5d all have to do with MatableGroups.)
                    5e. Draw an individual Line.
                    5f. Draw an individual Arc.
                    5g. Draw an individual Curve.
                    5h. Raise an exception if the returned matable fits none of the cases from 5b - 5h.
                    5i. The context drawing the Matables gets converted to a NumPy pixel array to be added to the pipe.
                    5j. The pixel array is written to the pipe."""

        self.mations = self.sort_mationlist() #1
        self.mations = self.merge_mations(self.mations) #2 
        self.pipe = self.prepare_for_rendering(end_dir) #3

        current_frame = 0
        for mation in self.mations: 
            for _ in mation.get_range_of_frames(): #5
                matable = mation.tick() #5a.
                #MatableGroup handling
                if isinstance(matable, MatableGroup): 
                    to_be_drawn: list = matable.get_matables_by_type(Line) #5b
                    for line in to_be_drawn: 
                        self.ctx.set_source_rgba(*line.color) #TODO, implement full customization for context
                        self.ctx.move_to(*line.get_point1())
                        self.ctx.line_to(*line.get_point2()) 
                        self.ctx.stroke_preserve()
                        self.ctx.fill() #5b
                    
                    to_be_drawn = matable.get_matables_by_type(Arc) #5c
                    for arc in to_be_drawn:
                        self.ctx.set_source_rgba(*arc.color)
                        self.ctx.new_sub_path()
                        self.ctx.arc(*arc.get_center(), arc.get_radius(), arc.get_angle_1(), arc.get_angle_2()) 
                        self.ctx.stroke_preserve()
                        self.ctx.fill() #5c

                    to_be_drawn = matable.get_matables_by_type(Curve) #5d
                    for curve in to_be_drawn: 
                        self.ctx.set_source_rgba(*curve.color)
                        self.ctx.move_to(curve.get_points()[0])
                        self.ctx.curve_to(*curve.get_points[1], *curve.get_points[2], *curve.get_points[3]) 
                        self.ctx.stroke_preserve()
                        self.ctx.fill() #5d

                elif isinstance(matable, Line): #53
                    self.ctx.set_source_rgba(*matable.color) 
                    self.ctx.move_to(*matable.get_point1())
                    self.ctx.line_to(*matable.get_point2()) 
                    self.ctx.stroke_preserve()
                    self.ctx.fill() #5e

                elif isinstance(matable, Arc): 
                    self.ctx.set_source_rgba(*matable.color)
                    self.ctx.new_sub_path()
                    self.ctx.arc(*matable.get_center(), matable.get_radius(), matable.get_angle_1(), matable.get_angle_2()) 
                    self.ctx.stroke_preserve()
                    self.ctx.fill() #5f

                elif isinstance(matable, Curve): #5g
                    self.ctx.set_source_rgba(*matable.color)
                    self.ctx.move_to(*matable.get_points()[0])
                    self.ctx.curve_to(*matable.get_points[1], *matable.get_points[2], *matable.get_points[3])
                    self.ctx.stroke_preserve()
                    self.ctx.fill() #5g

                else: 
                    raise Exception("The Matable returned by tick is neither a MatableGroup, or a Primitive, and thus can't be drawn.") #5h
                    #should this be a warning?

                width, height = self.get_dimensions()
                buf = self.surface.get_data()
                data = numpy.ndarray(shape=(height, width), 
                     dtype=numpy.uint32,
                     buffer=buf)

                if self.write_to_movie:
                    self.pipe.stdin.write(data) #5j.  TODO, arrange the data to ffmpeg-compatiable format.

        self.pipe.terminate()
                
                
            





    def write(self, /, tmpdir: str, enddir: str): 
        self.construct()
        self.save(tmpdir, enddir)

    def construct(self): 
        """Construct() lies at the heart of Synthesium. All Mations should be played in self.construct(), which the 
        internal pipeline looks for when creating an animation. """
        
