"""Mations, short for Animations, are designed to provide a way to make Matables move, simultaneously updating Matables
while also making calls to a Canvas's renderer"""
import warnings

from synthesium.utils.defaults import DEFAULT_FPS
from synthesium.matables.matable import *
from synthesium.utils.imports import *

class Mation:
    def __init__(self, target: Matable, start_second: int, start_frame, end_second: int, end_frame: int, rate_func):
        self.target = target
        class InvalidRuntimeError(Exception): #here in the case an invalid runtime is encountered, i.e, end time < start time.
                def __init__(self):
                    super().__init__(f"Beginning time was set to {start_second} seconds {start_frame} frames, \
                                       but end time was set to {end_second} seconds, {end_frame} frames")
        if start_second > end_second:  #here to prevend invalid runtimes
            raise InvalidRuntimeError()
        elif start_frame > end_frame: 
            if start_second == end_second:
                raise InvalidRuntimeError() #TODO, create a more intuitive system for seconds, frames, and minutes. The current one is ugly.

        else: 
            self.start_second = start_second; self.start_frame = start_frame
            self.end_second = end_second; self.end_frame = end_frame
        self.rate_func = rate_func

        self.fps = None #makes a lot of computation easier for this attribute to be here, instead of it being undefined until it gets
                        #played() in a Canvas
        self.total_frames = None

    def tick(self) -> Matable:
        """Tick gets called by Canvas to make the mation advance by one frame: tick updates the `target` Matable, and updates 
        the attribute self.current_frame, which is initialized ONLY after set_fps is called by Canvas, by the amount returned by the rate_function."""

    def set_start(self, start_second, start_frame): 
        self.start_second = start_second
        self.start_frame = start_frame
        return self

    def get_start(self): 
        return (self.start_second, self.end_frame)

    def get_start_second(self): 
        return self.start_second

    def get_start_frame(self, arg_fps=None): 
        if self.fps is None and arg_fps is None: 
            raise Exception("Both fps and self.fps are undefined. Either use mation.set_fps(), or canvas.play() to set it.")
        
        if self.fps is not None: 
            fps = self.fps #if fps is also defined, a warning will be raised and the argument fps will be used.

        if self.fps is None and arg_fps is not None and self.fps != fps: 
            warnings.warn("Fps was passed in as an argument even though self.fps was defined; using passed in fps and not self.fps.")
            fps = arg_fps

        if self.fps is None and arg_fps is not None: 
            fps=arg_fps

        return self.start_second*self.fps + self.start_frame 

    def set_end(self, end_second, end_frame): 
        self.end_second = end_second
        self.end_frame = end_frame
        return self

    def get_end(self): 
        return (self.end_second, self.end_frame)

    def get_end_second(self): 
        return self.end_second

    def get_end_frame(self, arg_fps=None): #while fps is optional, if self.fps has not been defined and fps is None, an exception will be thrown.
        if self.fps is None and arg_fps is None: 
            raise Exception("Both fps and self.fps are undefined. Either use mation.set_fps(), or canvas.play() to set it.")
        
        if self.fps is not None: 
            fps = self.fps #if fps is also defined, a warning will be raised and the argument fps will be used.

        if self.fps is None and arg_fps is not None and self.fps != fps: 
            warnings.warn("Fps was passed in as an argument even though self.fps was defined; using passed in fps and not self.fps.")
            fps = arg_fps
        
        if self.fps is None and arg_fps is not None: 
            fps = arg_fps

        return self.end_second*fps + self.end_frame 

    def set_fps(self, fps): 
        """Gets called in Canvas's internals when self.play(Mation) is called, allowing for fps, necessary for tick(), to be set 
           after instantiation"""
        
        assert(any([type(fps) == int, type(fps) == float])) #make sure fps is a number
        self.fps = fps
        self.current_frame = 0
        self.total_frames = self.end_second*fps + self.end_frame

    def get_range_of_frames(self): #mostly for internal use
        return range(self.get_start()[0]*self.fps+self.get_start()[1], self.get_end()[0]*self.fps+self.get_start()[1]+1)

    def __str__(self): 
        return f"Mation of type {type(self)}"

    def __repr__(self):
        return f"Mation({self.target}, {self.start_second}, {self.start_frame}, {self.end_second}, {self.end_frame}, {self.frame_addend}"
