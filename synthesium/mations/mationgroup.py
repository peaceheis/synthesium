from synthesium.utils.imports import *
from synthesium.mations.mation import Mation

class ConcurrentMation(Mation): #a Mation composed of Mations, used internally with Canvas so that it only has to process one Mation at a time, which simplifies a lot of logic.
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
        string = f"ConcurrentMation of type {self.__class__.__name__}, composed of" 
        for mation in self.mations: 
            string += f"\n\t Mation of type {mation.__class__.__name__} running from second {mation.get_start()[0]} frame {mation.get_start()[1]} \
                       to second {mation.get_end()[0]} frame {mation.get_end()[1]}"
        return string

    def __repr__(self) -> str:
        return self.__str__() #TODO create ConcurrentMation repr