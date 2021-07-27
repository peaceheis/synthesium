"""Enables multiple Matables (such as the primitives Line, Arc, and Curve), to make what functions as one Matable."""
from typing import Type

from synthesium.utils.imports import *
from synthesium.matables.matable import Matable
from synthesium.matables.primitives import *

class MatableGroup(Matable):
    def __init__(self, *matables: Union[tuple, list], **kwargs): 
        self.matables = matables
        self.points = [matable.get_points() for matable in matables] #recursively adds points
        self.configure(kwargs)
    
    def get_points(self): 
        return tuple([matable.get_points() for matable in self.matables])

    def get_matables(self): 
        return self.matables

    def set_matables(self): 
        self.matables = [matables.get_points() for matables in self.matables]
        self.points = [matable.get_points for matable in self.matables]

    def add_matable(self, matable): 
        self.matables += matable
        self.points += matable.get_points()

    def get_matables_by_type(self, type: "Type(Matable)"): 
        """[Used for recursively getting the Matables that make up a MatableGroup by type. Used internally to get all the Lines, 
            Curves, and Arcs that make up a MatableGroup.]

        Args:
            type Type(Matable): [the type of the Matable to be found.]

        Returns:
            [list]: [of all the Matables of the type found, if none found, returns an empty list.]
        """
        matables = []
        for matable in self.matables: #probably could be more compact as a list comprehension, but it's more readable this way in my opinon.
            if isinstance(matable, MatableGroup): 
                matables += matable.get_matables_by_type(type)

            elif isinstance(matable, type): 
                matables.append(matable)
        return matables

    def shift(self, amt): 
        self.matables = [matable.shift(amt) for matable in self.matables]
        self.points = [matable.get_points() for matable in self.matables]

    def rotate(self, degrees, center, rotates_clockwise = True): 
        self.matables = [matable.rotate(degrees, center, rotates_clockwise) for matable in self.matables]
        self.points = [matable.get_points() for matable in self.matables]

    def set_points(self, *points): #despite automatically raising an error on trying to run this, it's best to say WHY the error is being raised instead of python saying "invalid number of arguments"
        raise Exception("Using set_points() is not allowed with MatableGroups; add a Matable such as Line, Arc, or Curve, or else another MatableGroup.")
        #allowing MatableGroups to have their own points would be incompatible with the current rendering pipeline, which reduces everything to primitives.

    def __str__(self): 
        string = f"Matable Group of type {self.__class__.__name__}, consisting of "
        for matable in self.matables: 
            string += f"\n\t {matable.__str__()}"
        return string

