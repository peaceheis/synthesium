from typing import Type, Tuple, Union

from synthesium.matable.primitives import *


class MatableGroup(Matable):
    """Enables multiple Matables (such as the primitives Line, Arc, and Curve), to make what functions as one
    Matable. """

    def __init__(self, *matables: Union[tuple, list], **kwargs: dict) -> None:
        self.matables = matables
        self.points = []
        for matable in matables:
            self.points.extend(matable.get_points())
        self.configure(kwargs)

    def add_matable(self, matable: Matable) -> "MatableGroup":
        self.matables += matable
        self.points += matable.get_points()
        return self

    def get_matables_by_type(self, matable_type: Type) -> list:
        """[Used for recursively getting the Matables that make up a MatableGroup by type. Used internally to get all the Lines,
            Curves, and Arcs that make up a MatableGroup.]

        Args:
            type Type(Matable): [the type of the Matable to be found.]

        Returns:
            [list]: a list of all the Matables of the type found, if none found, returns an empty list.
        """
        matables = []
        # probably could be more compact as a list comprehension, but it's more readable this way.
        for matable in self.matables:
            if isinstance(matable, MatableGroup):
                matables += matable.get_matables_by_type(matable_type)

            elif isinstance(matable, matable_type):
                matables.append(matable)
        return matables

    def shift(self, amt):
        self.matables = [matable.shift(amt) for matable in self.matables]
        self.points = [matable.get_points() for matable in self.matables]

    def rotate(self, degrees, center, rotates_clockwise=True):
        self.matables = [matable.rotate(degrees, center, rotates_clockwise) for matable in self.matables]
        self.points = [matable.get_points() for matable in self.matables]

    # utils
    def get_points(self) -> "tuple":
        return tuple([matable.get_points() for matable in self.matables])

    def set_points(self, *points):
        """Setting individual points with a MatableGroup is not possible. Try setting the points of the individual
        Matables. """
        # despite automatically raising an error on trying to run this, it's best to say WHY
        # the error is being raised,
        # so we set the normal arguments.
        raise Exception(
            "Using set_points() is not allowed with MatableGroups; add a Matable such as Line, Arc, or Curve, "
            "or else another MatableGroup.")
        # allowing MatableGroups to have their own points would be incompatible with the current rendering pipeline,
        # which reduces everything to primitives.

    def matables(self):
        return self.matables

    def set_matables(self):
        self.matables = [matables.points() for matables in self.matables]
        self.points = [matable.points for matable in self.matables]

    def __str__(self):
        string = f"Matable Group of type {self.__class__.__name__}, consisting of "
        for matable in self.matables:
            string += f"\n\t {matable.__str__()}"
        return string
