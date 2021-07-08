"""Mations, short for Animations, are designed to provide a way to make Matables move, simultaneously updating Matables
while also making calls to a Scene's renderer"""

from ..matables.matables import *
from ..utils.imports import *

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



    def tick(self, current_frame, total_frames):
        """Tick gets called by Scene to make the mation advance by one frame: tick updates the `target` Matable, and updates 
        the attribute self.current_frame, which is initialized ONLY after set_fps is called by Scene, by the amount returned by the rate_function."""
        

    def set_start(self, start_second, start_frame): 
        self.start_second = start_second
        self.start_frame = start_frame
        return self

    def get_start(self): 
        return (self.start_second, self.end_frame)

    def get_start_second(self): 
        return self.start_second

    def get_start_frame(self): 
        return self.start_second*self.fps + self.start_frame 

    def set_end(self, end_second, end_frame): 
        self.end_second = end_second
        self.end_frame = end_frame
        return self

    def get_end(self): 
        return (self.end_second, self.end_frame)

    def get_end_second(self): 
        return self.end_second

    def get_end_frame(self, fps):
        return self.end_second*fps + self.end_frame

    def set_fps(self, fps): 
        """Gets called in Scene's internals when self.play(Mation) is called, allowing for fps, necessary for tick(), to be definited 
        after instantiation"""
        self.fps = fps
        self.current_frame = 0
        self.total_frames = self.end_second*fps + self.end_frame

    def get_range_of_frames(self): #mostly for internal use
        return range(self.get_start()[0]*self.fps+self.get_start()[1], self.get_end()[0]*self.fps+self.get_start()[1])


    def __str__(self): 
        return f"Mation of type {type(self)}"

    def __repr__(self):
        return f"Mation({self.target}, {self.start_second}, {self.start_frame}, {self.end_second}, {self.end_frame}, {self.frame_addend}"




class ConcurrentMation(Mation): #a Mation composed of Mations, used for Scene so that it only has to process one Mation at a time
    def __init__(self, mations: "Union[list[Mation], tuple[Mation]]"):
        self.mations = (mation for mation in mations)
        self.start = sorted(mations, key=Mation.get_start)[0]
        self.end = sorted(mations, key=Mation.get_end, reverse=True)[0]

    def tick(self, rate_func): 
        return (mation.tick(rate_func) for mation in self.mations) #returns a tuple of returned mations for each ticked mation

    def split(self, second, frame, fps): 
        self.mations = [mation.add_split(second, frame) for mation in self.mations]
        return ConcurrentMation(self.mations)

    def __str__(self): 
        return f"ConcurrentMation of type {type(self)}, with Sub-Mations {self.mations}"

    def __repr__(self) -> str:
        return self.__str__() #TODO create ConcurrentMation repr


#some predefined Mations
class Move(Mation):
    def __init__(self, target: Matable, amount: tuple, start_second: int, start_frame, end_second, end_frame, rate_func):
        super().__init__(target, start_second, start_frame, end_second, end_frame, rate_func)
        self.amount = amount

    def tick(self): 
        single_frame_amount = [amt/self.total_frames for amt in self.amount]
        adjusted_frame_amount = [amt * self.rate_func(self.current_frame, self.total_frames) for amt in single_frame_amount]
        self.current_frame += 1
        return self.target.shift(adjusted_frame_amount) 

    def __repr__(self): 
        return f"Mation({self.target}, {self.amount}, {self.start_second}, {self.start_frame}, {self.end_second}, {self.end_frame}"
