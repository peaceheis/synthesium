import os
import os.path
from synthesium.utils.useful_functions import linear_increase
from synthesium.matable.shapes import Circle, Triangle
from synthesium.utils.defaults import DEFAULT_FPS, FFMPEG_BIN
import subprocess

import numpy
import cairo
from cairo import ImageSurface



from synthesium.utils.imports import *
from synthesium.matable.primitives import Line, Arc, Curve #Line, Arc, Curve
from synthesium.matable.matable import Matable
from synthesium.matable.matablegroup import MatableGroup
from synthesium.mation.mation import Mation
from synthesium.mation.mationgroup import MationGroup

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

    def add_mations(self, *mations): 
        """calling self.add(mation) doesn't do much besides add it to the list of Mations to be processed. The heavy lifting is done when
        Canvas.write() is called, outside the class definition."""
        for mation in mations: 
            mation.set_fps(self.fps)
            self.mations.append(mation)


    #auxiliary functions to save()

    def sort_mationlist(self):
        """Sorts the mationlist by start frame. It assumes that the Mations have been added, and therefore have
           had their fps set, because otherwise, how would they be in self.mations in the first place?"""
        
        return sorted(self.mations, key= Mation.get_start_frame)

    def merge_mations(self):
        """Take all the mations in a list and compress them into a list of MationGroup to remove any overlap between 
           Mations. This is used with Canvas to ensure only one Mation (or MationGroup) has to be handled at a time."""

        mationlist = self.mations #it's a bit more intuitive to have a separate list
        if not mationlist: 
            raise Exception(f"No mations were provided to Canvas {self.__class__.__name__}, use add_mation to do so.")

        def overlap_exists_between(mation1: Mation, mation2: Mation): 
            return mation2.get_start_frame() >= mation1.get_start_frame() and mation2.get_start_frame() <= mation1.get_end_frame() 
             #check if the second mation starts before or when the first mation ends, but starts after or when the first mation starts.
        
        if len(mationlist) == 1:
            return mationlist

        if len(mationlist) == 2:
            mation1 = mationlist[0]
            mation2 = mationlist[1] 
            if overlap_exists_between(mation1, mation2): 
                return [MationGroup(mation1, mation2, fps=self.fps)]
            return mationlist

        #assumes len 3 or longer
        merged_list = []
        current_group = MationGroup(fps=self.fps)
        #check the first entry for overlap 
        mation1 = mationlist[0]
        mation2 = mationlist[1]
        if overlap_exists_between(mation1, mation2):
            current_group.add(mation1) #the second will be added during the loop
        else: #no overlap
            merged_list.append(mation1)

        for i in range(len(mationlist)-2): #exclude first and last mations
            before = mationlist[i]
            mation = mationlist[i+1]
            after = mationlist[i+2]

            if overlap_exists_between(before, mation): 
                current_group.add(mation)
            
            elif overlap_exists_between(mation, after): #a new group should be probably be started in this case, but to be sure:
                if len(current_group.get_mations()) == 0: #no point in packaging an empty list, and in fact it'll break things.
                    pass #there's no need to reset current_group, it's already initialized.
                elif len(current_group.get_mations()) == 1: #if there's one, just add the contained Mation - no unnecessary MationGroups stealing memory.
                    mationlist.append(*current_group.get_mations()) 
                    current_group = MationGroup(fps=self.fps) #reset the group with the current mation.
                elif len(current_group.get_mations() > 1): 
                    mationlist.append(current_group) 
                    current_group = MationGroup(mation, fps=self.fps) 
                    #if the group is longer than 1, add the group to the list and start a new one with the current mation.
            
            else: #no overlap, this Mation's quite the special little snowflake innit?
                mationlist.append(mation)
    
        #last mation handling: 
        before = mationlist[-2]
        mation = mationlist[-1] 
        #see above for explanations
        if overlap_exists_between(before, mation): 
            if len(current_group.get_mations()) == 0: 
                pass
            elif len(current_group.get_mations()) == 1: 
                mationlist.append(*current_group.get_mations()) 
                current_group = MationGroup(fps=self.fps) 
            elif len(current_group.get_mations() > 1): 
                mationlist.append(current_group) 
                current_group = MationGroup(mation, fps=self.fps)
        
        #lastly, handle packaging of the final group
        if not len(current_group.get_mations()) == 0: 
            mationlist.append(current_group)

        return mationlist #all done

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
            '-i', '-',  # The imput comes from a pipe
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
        ]  


            
        command += [end_dir] #TODO, implement partial movie files à la Manim.
        return subprocess.Popen(command, stdin=subprocess.PIPE)
        #credit to Manim (https://github.com/3b1b/manim). I adapted this code from scene_file_writer.py, in the cairo-backend branch. Brilliant code there.

    def draw_line(self, line): 
        self.ctx.set_source_rgba(*line.config["color"]) #TODO, implement full customization for context
        self.ctx.new_sub_path()
        self.ctx.move_to(*line.get_point1())
        self.ctx.line_to(*line.get_point2()) 
        self.ctx.stroke_preserve()
        self.ctx.fill() #5b

    def draw_arc(self, arc): 
        self.ctx.set_source_rgba(*arc.config["color"])
        self.ctx.new_sub_path()
        self.ctx.arc(*arc.get_center(), arc.get_radius(), arc.get_angle1(), arc.get_angle2()) 
        self.ctx.stroke_preserve()
        self.ctx.fill() #5c

    def draw_curve(self, curve):
        self.ctx.set_source_rgba(*curve.config["color"])
        self.ctx.new_sub_path()
        self.ctx.move_to(*curve.get_points()[0])
        self.ctx.curve_to(*curve.get_points()[0], *curve.get_points()[1], *curve.get_points()[2], *curve.get_points()[3]) 
        self.ctx.stroke_preserve()
        self.ctx.fill() #5d

    def draw_matable_group(self, mgroup):
        to_be_drawn: list = mgroup.get_matables_by_type(Line)
        for line in to_be_drawn: 
            self.draw_line(line)

        to_be_drawn: list = mgroup.get_matables_by_type(Arc)
        for arc in to_be_drawn: 
            self.draw_arc(arc)

        to_be_drawn:list = mgroup.get_matables_by_type(Curve)
        for curve in to_be_drawn: 
            self.draw_curve(curve)

    def save(self, end_dir: str): 
        """This is where all the rendering work gets done. The steps are as follows:
                1. The mation list is constructed (by calling the user-defined construct()), and sorted by start frame,
                2. A compressed list where any overlapping Mations are made into a MationGroup is generated,
                3. After verification of the end directory, a pipe is opened to ffmpeg to string together all the frames.
                Then things get interesting. 
                5. The animation gets rendered via loop: 
                    5a. Make the animation progress 1 frame.
                    For every matable returned by a Mation: 
                        5b. If it's a MatableGroup, break it down into its components and draw them.
                        5c. If it's a Line, draw it.
                        5d. If it's an Arc, draw it.
                        5e. If it's a Curve, draw it.
                    5f. Raise an exception if the returned matable fits none of the cases from 5b - 5h.
                    5g. The context drawing the Matables gets converted to a NumPy pixel array to be added to the pipe.
                    5h. The pixel array is written to the pipe.
                6. The video is written."""

        if len(self.mations) == 0: 
            raise Exception("No Mations were added!")
        self.mations = self.sort_mationlist() #1
        self.mations = self.merge_mations() #2 
        self.pipe = self.open_pipe_for_rendering(end_dir) #3

        for mation in self.mations: 
            print(f"Processing mation {mation}")
            for _ in mation.get_range_of_frames(): #5
                matable = mation.tick() #5a.
                #MatableGroup handling
                if isinstance(matable, MatableGroup): 
                    self.draw_matable_group(matable) #5b

                elif isinstance(matable, Line): 
                    self.draw_line(matable) #5c 

                elif isinstance(matable, Arc): 
                    self.draw_arc(matable) #5d

                elif isinstance(matable, Curve): 
                    self.draw_curve(matable) #5e

                else: 
                    raise Exception(f"The Matable returned by the tick method of mation {mation} is neither a MatableGroup, or a Primitive, and thus can't be drawn.") #5f
                    #should this be a warning?

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
        

