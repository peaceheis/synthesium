from typing import Iterable
from ..utils.standard_imports import *
from ..matables.matables import Matable, Circle, Line
from ..mations.mations import Mation, ConcurrentMation, Move

class Scene(): 
    def __init__(self, *, background_color=BLACK, fps=24): 
        self.mations = []
        self.background_color = background_color
        self.fps = fps

    def play(self, *mations): 
        """calling self.add(mation) doesn't do much besides add it to the list of Mations to be processed. The heavy lifting is done when
        Scene.view() is called, outside the class definition."""
        if type(mations) == Mation:
            self.mations.append(mations)
        
        if all([type(mation) for mation in mations]): 
            self.mations.append(*mations)
        

    def view(self): 
        pass

    def build_animation_hierarchy(self): 
        self.construct()
        """
        except Exception: 
            class NoConstructMethodError(Exception): 
                def __init__(self): 
                    super().__init__("No construct method found for Scene")
            raise NoConstructMethodError
        """
        mation_sorter = lambda mation: mation.get_start()[0]*self.fps + mation.get_start()[1]
        return sorted(self.mations, key=mation_sorter) #TODO, implement the ConcurrentMation building

    def construct(self): 
        """Construct() lies at the heart of Synthesium. All Mations should be played in self.construct(), which the 
        internal pipeline looks for when creating an animation. """
        pass


class TestScene(Scene): 
    def construct(self): 
        self.play(Move(Circle((0, 0), 1), amount=(1, 0, 0, 0), start_second=1, start_frame=0, end_second=2, end_frame=0))
        self.play(Move(Circle((0, 0), 1), amount=(1, 0, 0, 0), start_second=0, start_frame=0, end_second=1, end_frame=0))
        self.play(Move(Line((0, 0), (0,1)), amount=(1, 0, 0, 1), start_second=0, start_frame=3, end_second=3, end_frame=1))

test = TestScene()
print(test.build_animation_hierarchy())
             
            
