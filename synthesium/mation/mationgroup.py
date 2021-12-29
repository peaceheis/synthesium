from synthesium.mation.timemarker import TimeMarker
from synthesium.matable.matablegroup import MatableGroup
from synthesium.mation import mation
from synthesium.utils.imports import *
from synthesium.mation.mation import Mation


class MationGroup(Mation): 
    """a Mation composed of Mations, used internally with Canvas so that it only has to process one Mation at a time, which simplifies a lot of logic."""
    
    def __init__(self, *mations, fps=None):
        self.mations = [mation for mation in mations]
        if len(mations) > 0: #to prevent an empty MationGroup to run into issues with bound updating
            self.update_bounds()
        else: 
            self.start = TimeMarker(0, 0, 0)
            self.end = TimeMarker(0, 0, 0)
        self.fps = fps
        if self.fps is not None: 
            self.total_frames = self.end.time_as_int(self.fps) - self.start.time_as_int(self.fps) + 1
        else: 
            self.total_frames = None

    def update_bounds(self): 
        self.start = sorted(self.mations, key=Mation.get_start)[0].get_start()
        self.end = sorted(self.mations, key=Mation.get_end, reverse=True)[0].get_end()

    def tick(self): 
        return MatableGroup(*[mation.tick() for mation in self.mations]) #returns a MatableGroup of returned mations for each ticked mation

    def __str__(self): 
        string = f"MationGroup of type {self.__class__.__name__}, composed of" 
        for mation in self.mations: 
            string += f"\n\t Mation of type {mation.__class__.__name__} running from {self.start} to {self.end}"
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
        #because Python uses reference counting along with garbage collection, the mations that don't make it into the new list should
        #get deleted.
    
    def set_start(self, start: TimeMarker):
        raise Exception("Setting start and end is not allowed with Mations of type MationGroup.")
    
    def set_end(self, end: TimeMarker):
        raise Exception("Setting start and end is not allowed with Mations of type MationGroup.")

    def get_mations(self): 
        return self.mations

    def __repr__(self) -> str:
        return self.__str__() #TODO create MationGroup repr

    