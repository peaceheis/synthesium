"""Mations, short for Animations, are designed to provide a way to make Matables move, simultaneously updating Matables
while also making calls to Canvas's renderer"""
import copy
import warnings
from collections import namedtuple

from synthesium.mation.timemarker import TimeMarker
from synthesium.matable.matable import *
from synthesium.utils.imports import *


class Mation:
    def __init__(self, target: Matable, start: TimeMarker, end: TimeMarker, rate_func=constant):
        self.target = target 
        self.validate_runtimes(start, end)
        self.start = start
        self.end = end    
        self.rate_func = rate_func

        self.fps = None #makes a lot of computation easier for this attribute to be here, instead of it being undefined until it gets
                        #played() in a Canvas
        if self.fps is not None: 
            self.total_frames = self.end.time_as_int(self.fps) - self.start.time_as_int(self.fps) + 1
        else: 
            self.total_frames = None

    def tick(self) -> Matable:
        """Tick gets called by Canvas to make the mation advance by one frame: tick updates the `target` Matable, and updates 
        the attribute self.current_frame, which is initialized ONLY after set_fps is called by Canvas, by the amount returned by the rate_function."""
    
    def get_start(self) -> TimeMarker: 
        return self.start

    def set_start(self, marker: TimeMarker) -> "Mation": 
        self.validate_runtimes()
        self.start = marker
        return self

    def get_start_as_int(self) -> int: 
        return self.start.time_as_int(self.fps)
        
    def get_end(self) -> TimeMarker: 
        return self.end

    def set_end(self, marker: TimeMarker) -> "Mation": 
        self.validate_runtimes()
        self.end = marker
        return self

    def get_end_as_int(self) -> int: 
        return self.end.time_as_int()

    def set_fps(self, fps): 
        """Gets called in Canvas's internals when self.play(Mation) is called, allowing for fps, necessary for tick(), to be set 
           after instantiation"""
        
        assert(any([type(fps) == int, type(fps) == float])) #make sure fps is a number
        if self.start.get_frame() > fps: 
            raise Exception(f"Mation's start frame is greater than FPS. ({self.start.get_frame()} > {fps})")
        if self.end.get_frame() > fps: 
            raise Exception(f"Mation's start frame is greater than FPS. ({self.end.get_frame()} > {fps})")
        self.fps = fps
        self.current_frame = 0
        self.total_frames = self.end.time_as_int(self.fps) - self.start.time_as_int(self.fps) + 1

    def get_range_of_frames(self): #mostly for internal use
        return range(self.total_frames)

    def validate_runtimes(self, start: TimeMarker, end: TimeMarker): 
        class InvalidRuntimeError(Exception): #here in the case an invalid runtime is encountered, i.e, end time < start time.
                def __init__(self):
                    super().__init__(f"Beginning time was set to {start}, \
                                       but end time was set to {end}")
        if not start < end: 
            raise InvalidRuntimeError()
    
    def copy(self): 
        return copy.deepcopy(self) #allows for creating small variants of a matable with method chaining

    def __str__(self): 
        return f"Mation of type {type(self)}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.target}, {self.start_second}, {self.start_frame}, {self.end_second}, {self.get_end_in_frame_form})"
