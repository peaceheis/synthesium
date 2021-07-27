"""Predefined Matables made of the Primitives Line, Arc, and Curve"""
from typing import Union

from synthesium.utils.imports import *
from synthesium.matables.matable import Matable
from synthesium.matables.matablegroup import MatableGroup
from synthesium.matables.primitives import * #Arc, Line, Curve

class Circle(Arc): 
    def __init__(self, center: tuple, radius: int, color = PURE_GREEN): 
        super().__init__(center, radius, 360)
        self.circumference = pi * (radius **2) 
        self.color = color
    
    def shift(self, amt: tuple):
        center = self.center
        new_x_value = center[0] + amt[0] - amt[1]
        new_y_value = center[1] + amt[2] - amt[3]
        self.center = (new_x_value, new_y_value)
        return self

    def get_center(self) -> tuple: 
        return self.center
    
    def set_center(self, center: tuple):
        self.center = center 
        return self

    def get_radius(self) -> Union[int, float]: 
        return self.radius 

    def set_radius(self, radius: Union[int, float]): 
        self.radius = radius
        return self

    def __repr__(self): 
        return f"Circle({self.center}, {self.radius})"

#slightly more involved geometry goes here.
class Polygon(MatableGroup) : 
    """Base class for Polygons, as the name suggests. Most of its functionality lies in being able to converting points to Lines to direct to the
       MatableGroup constructor."""
    def __init__(self, *points, **kwargs): 
        default_config = {
            "line_width": 10, 
            "color": PURE_RED, 
            "fill_color": PURE_GREEN
        }

        matables = [] 
        for i in range(len(points) - 1):  #using 1 less because the last point has to connect to the first point, which requires special handling.
            matables += Line(points[i], points[i+1])
        matables += Line(points[-1], points[0]) #connect last element and first element.

        super().__init__(*matables, **kwargs) #let MatableGroup handle the rest.
        self.configure(default_config, **kwargs) #while MatableGroup also has configure() in the init, it's best to update with Polygon's default config.
    
    def __repr__(self) : 
        return f"Polygon({self.points})"

class Quadrilateral(Polygon):
    """Class for any Quadrilaterals, inheriting from Polygon. """
    def __init__(self, point1, point2, point3, point4, **kwargs): 
        """Instead of making the user create each individual Matable, all the user has to do is give the points and Synthesium generates the rest."""
        super().__init__(point1, point2, point3, point4, **kwargs)

class Square(MatableGroup):
    """A class that enforces all the side lengths to be the same."""
    def __init__(self, center, side_length, **kwargs): 
        """[to make sure that a square is generated, the center and side length are given, and the points are generated by 
            going out half the side length in the +x +y, +x, -y, -x, -y, and -x, +y directions.]

        Args:
            center ([tuple]): [the x and y coordinates of the center.]
            side_length ([Union[float, int]]): [the length of the sides (obviously)]
        """
        half_side_length = side_length/2
        points = [
            center[0] + half_side_length, center[1] + half_side_length, #positive x and y
            center[0] - half_side_length, center[0] + half_side_length, #negative x, positive y
            center[0] - half_side_length, center[0] - half_side_length, #negative x and y
            center[0] + half_side_length, center[0] - half_side_length,  #positive x and negative y
        ]

        super().__init__(*points, **kwargs) 

class Triangle(MatableGroup): 
    """I would think the name is self-explanatory."""
    def __init__(self, point1, point2, point3, **kwargs): 
        super().__init__(point1, point2, point3, **kwargs)



