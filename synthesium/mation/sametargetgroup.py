from synthesium.utils.imports import *
from synthesium.mation.mationgroup import MationGroup
from synthesium.matable.matablegroup import MatableGroup

class SameTargetGroup(MationGroup): 
    """For when you want multiple Mations to target the same Matable."""

    def __init__(self, target, *mations, fps=None): 
        super().__init__(*mations, fps=fps)
        self.target = target

    def tick(self): 
        self.current_frame += 1 
        for mation in self.mations: 
            if mation.is_active_at_frame(self.current_frame):
                mation.tick()

        return self.target