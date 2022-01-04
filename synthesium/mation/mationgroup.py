from synthesium.mation.timestamp import TimeStamp
from synthesium.matable.matablegroup import MatableGroup
from synthesium.mation import mation
from synthesium.utils.imports import *
from synthesium.mation.mation import Mation


class MationGroup(Mation): 
    """a Mation composed of Mations, used internally with Canvas so that it only has to process one Mation at a time, which simplifies a lot of logic."""
    
    def __init__(self, *mations, fps=None):
        self.should_call_pre_tick = False
        self.mations = [mation for mation in mations]
        self.pre_tickers = [mation for mation in mations if mation.should_call_pre_tick]
        if len(self.pre_tickers) > 0: 
            self.should_call_pre_tick = True
        
        self.current_frame = 0
        if len(mations) > 0: #to prevent an empty MationGroup to run into issues with bound updating
            self.update_bounds()
        else: 
            self.start = TimeStamp(0, 0, 0)
            self.end = TimeStamp(0, 0, 0)
        self.fps = fps
        if self.fps is not None: 
            self.total_frames = self.end.time_as_int(self.fps) - self.start.time_as_int(self.fps) + 1
        else: 
            self.total_frames = None

    def update_bounds(self): 
        start = sorted(self.mations, key=Mation.get_start)[0].get_start()
        end = sorted(self.mations, key=Mation.get_end, reverse=True)[0].get_end()
        if not end > start: 
            raise Exception("Mation's end comes before start")
        self.start = start
        self.end = end

    def pre_tick(self): 
        for mation in self.pre_tickers: 
            mation.pre_tick()

    def tick(self): 
        self.current_frame += 1 #TODO fool! You didn't implement current_frame for Groups!
        return MatableGroup(*[mation.tick() for mation in self.mations]) #returns a MatableGroup of returned mations for each ticked mation

    def __str__(self): 
        string = f"MationGroup of type {self.__class__.__name__}, composed of" 
        for mation in self.mations: 
            string += f"\n\t Mation of type {mation.__class__.__name__} running from {mation.start} to {mation.end}"
        return string

    def add(self, *mations): 
        assert(all([isinstance(mation, Mation) for mation in mations])) #ensure all the arguments given are Mations 
        self.mations.append(*mations)
        self.update_bounds()

    def remove_mation_by_index(self, index):  #in case a Mation hasn't been bound to a variable.
        del self.mations[index] #if there's an IndexError, Python will let the user know.

    def remove(self, *mations): 
        """Remove Mations from the mation list"""
        self.mations = [mation for mation in self.mations if mation not in mations] #regenerate mationlist without the mations in the list.
        self.update_bounds()
        
    
    def set_start(self, start: TimeStamp):
        raise Exception("Setting start and end is not allowed with Mations of type MationGroup.")
    
    def set_end(self, end: TimeStamp):
        raise Exception("Setting start and end is not allowed with Mations of type MationGroup.")

    def get_mations(self): 
        return self.mations

    def __repr__(self) -> str:
        return self.__str__() #TODO create MationGroup repr

    