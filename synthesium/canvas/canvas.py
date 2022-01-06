import os
import os.path
import subprocess

import numpy
import cairo
from cairo import ImageSurface

from synthesium.utils.imports import *
from synthesium.matable.primitives import Line, Arc, Curve 
from synthesium.matable.matablegroup import MatableGroup
from synthesium.mation.mation import Mation
from synthesium.mation.mationgroup import MationGroup
from synthesium.utils.defaults import DEFAULT_FPS, FFMPEG_BIN

class Canvas():  
    """The canvas acts as the entry point between the user and Synthesium. The user creates a class that inherits from Canvas,
       overrides construct, and then instantiates their custom class, then runs save("end_directory"), which returns the 
       finished video. All the rendering goes on in here, breaking MatableGroups down to Primitives, and then cairo draws the 
       primitives. In addition, animation goes on here, by calling tick on every active Mation."""

    def __init__(self, /, background_color=(0, 0, 0, 1), fps=DEFAULT_FPS, canvas_size=(DEFAULT_FRAME_WIDTH, DEFAULT_FRAME_HEIGHT), \
                 frame_size = (DEFAULT_FRAME_WIDTH, DEFAULT_FRAME_HEIGHT)): #TODO, make a better default frame size
        self.mations = []
        self.background_color = background_color
        self.fps = fps
        self.width, self.height = canvas_size #canvas size is the size of the canvas in which everything will be drawn...
        self.frame_width, self.frame_height = frame_size #...frame size is the size of the output video. this allows for things like panning cameras.
        self.count = 0

        #cairo things
        self.surface = ImageSurface(cairo.Format.ARGB32, self.width, self.height)
        self.ctx = cairo.Context(self.surface)
        self.initialize_surface()
    
    def get_dimensions(self): 
        return (self.width, self.height) #TODO work on capturing

    def initialize_surface(self): 
        #initialize background color
        self.ctx.move_to(0, 0)
        self.ctx.set_source_rgba(*self.background_color[:3], self.background_color[3])
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

    def add(self, *mations): 
        self.count += 1
        """calling self.add(mation) doesn't do much besides add it to the list of Mations to be processed. The heavy lifting is done when
        Canvas.write() is called, outside the class definition."""
        for mation in mations: 
            mation.set_fps(self.fps)
            self.mations.append(mation)

    #auxiliary functions to save()

    def sort_mationlist(self):
        """Sorts the mationlist by start frame. It assumes that the Mations have been add()ed, and therefore have
           had their fps set."""
        
        return sorted(self.mations, key=Mation.get_start_as_int)

    def merge_mations(self):
        """Take all the mations in a list and compress them into a list of MationGroup to remove any overlap between 
           Mations. This is used with Canvas to ensure only one Mation (or MationGroup) has to be handled at a time."""
        print(self.mations)
        return self.mations #TODO write a functioning mation merging method

    def open_pipe_for_rendering(self, end_dir): 
        if not os.path.exists(os.path.split(end_dir)[0]):
            raise Exception(f"directory {end_dir} provided to Canvas {self.__class__.__name__} does not exist.")

        command = [
            FFMPEG_BIN, 
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', str(self.frame_width) + 'x' + str(self.frame_height),  # size of one frame
            '-pix_fmt', 'rgba',
            '-r', str(self.fps),  # frames per second
            '-i', '-',  # The input comes from a pipe
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
        ]  
   
        command += [end_dir] #TODO, implement partial movie files à la Manim.
        return subprocess.Popen(command, stdin=subprocess.PIPE)
        # credit to Manim (https://github.com/3b1b/manim). 
        # I adapted this code from scene_file_writer.py, in the cairo-backend branch. Brilliant code there.

    def draw_line(self, line: Line): 
        self.ctx.set_source_rgba(*line.config["color"]) #TODO, implement full customization for context
        self.ctx.set_line_width(line.config["line_width"])
        self.ctx.new_sub_path()
        self.ctx.move_to(*line.get_point1().as_tuple())
        self.ctx.line_to(*line.get_point2().as_tuple()) 
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgba(*line.config["fill_color"])
        self.ctx.fill() #5b

    def draw_arc(self, arc: Arc): 
        self.ctx.set_source_rgba(*arc.config["color"])
        self.ctx.set_line_width(arc.config["line_width"])
        self.ctx.new_sub_path()
        if arc.negative: 
            self.ctx.arc_negative(*arc.get_center().as_tuple(), arc.get_radius(), arc.get_angle1(), arc.get_angle2()) 
        else: 
            self.ctx.arc(*arc.get_center().as_tuple(), arc.get_radius(), arc.get_angle1(), arc.get_angle2()) 
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgba(*arc.config["fill_color"])
        self.ctx.fill() #5c

    def draw_curve(self, curve: Curve):
        self.ctx.set_source_rgba(*curve.config["color"])
        self.ctx.set_line_width(curve.config["line_width"])
        self.ctx.new_sub_path()
        self.ctx.move_to(*curve.get_points()[0].as_tuple())
        self.ctx.curve_to(*curve.get_points()[0].as_tuple(), *curve.get_points()[1].as_tuple(), *curve.get_points()[2].as_tuple(), *curve.get_points()[3].as_tuple()) 
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgba(*curve.config["fill_color"])
        self.ctx.fill() #5d

    def draw_matable_group(self, mgroup: MatableGroup):
        to_be_drawn: list = mgroup.get_matables_by_type(Line)
        for line in to_be_drawn: 
            self.draw_line(line)

        to_be_drawn: list = mgroup.get_matables_by_type(Arc)
        for arc in to_be_drawn: 
            self.draw_arc(arc)

        to_be_drawn:list = mgroup.get_matables_by_type(Curve)
        for curve in to_be_drawn: 
            self.draw_curve(curve)

    def draw_vector_matables(self, matable): 
        #MatableGroup handling
        if isinstance(matable, MatableGroup): 
            self.draw_matable_group(matable) #5b
            return True

        elif isinstance(matable, Line): 
            self.draw_line(matable) #5c
            return True 

        elif isinstance(matable, Arc): 
            self.draw_arc(matable) #5d
            return True

        elif isinstance(matable, Curve): 
            self.draw_curve(matable) #5e
            return True

        else: 
            return False

    def save(self, end_dir: str): 
        """This is where all the rendering work gets done. The steps are as follows:
                1. The mation list is constructed (by calling the user-defined construct()), and sorted by start frame,
                2. A compressed list where any overlapping Mations are made into a MationGroup is generated,
                3. After verification of the end directory, a pipe is opened to ffmpeg to string together all the frames.
                5. The animation then gets rendered via loop: 
                    5a. Make the animation progress 1 frame, and get all the matables to be drawn in that frame.
                    5b. Break them down, and render the primitives Line, Arc, and Curve.
                6. The video is written."""

        if len(self.mations) == 0: 
            raise Exception("No Mations were added!")
        self.mations = self.sort_mationlist() #1
        self.mations = self.merge_mations() #2 
        self.pipe = self.open_pipe_for_rendering(end_dir) #3

        for mation in self.mations: 
            print(f"Processing mation {mation}")
            if(mation.should_call_pre_tick): 
                    mation.pre_tick()
            for _ in mation.get_range_of_frames(): #5
                print(f"processing frame {mation.current_frame}")
                matable = mation.tick() #5a.
                valid = self.draw_vector_matables(matable) #5b
                if not valid: 
                    raise Exception(f"Matable {matable} returned by mation {mation} not drawable.")
                
                width, height = self.get_dimensions()
                buf = self.surface.get_data()
                data = numpy.ndarray(shape=(height, width), 
                    dtype=numpy.uint32,
                    buffer=buf)
                self.pipe.stdin.write(data.tobytes()) #5g.

                self.initialize_surface()

        self.pipe.stdin.close()
        self.pipe.wait()
        self.pipe.terminate() #6
                
    def write(self, enddir: str): #funny how the most involved method is the shortest.
        self.construct()
        self.save(enddir)

    def construct(self): 
        """Construct() lies at the heart of Synthesium. All Mations should be played in self.construct(), which the 
        internal pipeline looks for when creating an animation. This idea from this comes from 3b1b's Manim. Check it out at https://github.com/3b1b/manim"""



