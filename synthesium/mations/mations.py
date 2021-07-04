"""Mations, short for Animations, are designed to provide a way to make Matables move, simultaneously updating Matables
while also making calls to a Scene's renderer"""

from ..matables.matables import *
from ..utils.standard_imports import *

class Mation:
    def __init__(self, target: Matable, start_second: int, start_frame, end_second: int, end_frame: int, frame_addend: int=0):
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
        self.frame_addend = frame_addend #here to be able to split Mations, used by Scene to break and combine Mations as necessary.

    def tick(self, progress: tuple, rate_func):
        """The tick() function is slightly complicated:
        First, it takes a progress tuple in the form of (current_frame, total_frames),
        Next, it will generate the average amount of change of whatever attribute will be changed:
        simply put, it's generating an average dy over the total amount of frames. 
        Then, it will put that average amount through a lambda, `rate_func`, that will
        tell what proportion (generally 0<=x<=2, with 1 being the average change amount) of that amount it should output, allowing for dynamic rates of change of progress
        through the animation.
        There is an important stipulation: the integral from 0 to total_frames of the rate_func 
        must *EXACTLY* equal the integral from 0 to total_frames the generated average.
        In other words, runtime must stay constant regardless of usage of a rate_func. 
        After that, the Mation outputs a Matable modified by the average amount multiplied by the proportion output, and tick() is done."""
        pass

    def set_start(self, start_second, start_frame): 
        return Mation(self.target, start_second, start_frame, self.end_second, self.end_frame, self.start_frame)

    def get_start(self): 
        return (self.start_second, self.end_frame)

    def set_end(self, end, end_frame): 
        return Mation(self.target, self.start_second, self.start_frame, end, end_frame, self.start_frame)

    def get_end(self): 
        return (self.end_second, self.end_frame)

    def add_split(self, second, frame): 
        """Largely here for ConcurrentMation compatability, but if no Mation besides the current one is wanted, this is the method to use."""
        self.stop_second = second
        self.stop_frame = frame
        return self

    def split(self, second, frame, fps): 
        """Split doesn't actually split the Mation, but rather creates a new Mation that will begin where the other leaves off, and 
        creates two special attributes, split_second and split_frame, that show where the Mation is meant to stop. 
        This is here because for optimization, Scene sometimes needs to create two separate Mations from one Mation."""
        self.add_split(second, frame)
        return Mation(self.target, self.start_second, self.start_frame, self.end_second, self.end_frame, frame_addend=second*fps+frame)

    def __str__(self): 
        return f"Mation of type {type(self)}"

    def __repr__(self):
        return f"Mation({self.target}, {self.start_second}, {self.start_frame}, {self.end_second}, {self.end_frame}, {self.frame_addend}"

class ConcurrentMation(Mation): #a Mation composed of Mations, used for Scene so that it only has to process one Mation at a time
    def __init__(self, mations: "Union[list[Mation], tuple[Mation]]"):
        self.mations = (mation for mation in mations)
        self.start = sorted(mations, key=Mation.get_start)[0]
        self.end = sorted(mations, key=Mation.get_end, reverse=True)[0]

    def tick(self, progress: tuple, rate_func): 
        return (mation.tick() for mation in self.mations) #returns a tuple of returned mations for each ticked mation

    def split(self, second, frame, fps): 
        self.mations = [mation.add_split(second, frame) for mation in self.mations]
        return ConcurrentMation(self.mations)

    def __str__(self): 
        return f"ConcurrentMation of type {type(self)}, with Sub-Mations {self.mations}"

    def __repr__(self) -> str:
        return self.__str__() #TODO create ConcurrentMation repr


#some predefined Mations
class Move(Mation):
    def __init__(self, target: Matable, amount: tuple, start_second: int, start_frame, end_second, end_frame, frame_addend=0):
        super().__init__(target, start_second, start_frame, end_second, end_frame, frame_addend)
        self.amount = amount

    def tick(self, progress, rate_func): 
        total_frames = progress[1]
        single_frame_amount = (amt/total_frames for amt in self.amount)
        adjusted_frame_amount = single_frame_amount * rate_func(progress)
        return self.target.move(adjusted_frame_amount) 

    def __repr__(self): 
        return f"Mation({self.target}, {self.amount}, {self.start_second}, {self.start_frame}, {self.end_second}, {self.end_frame}, {self.frame_addend}"
