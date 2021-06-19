from math import sqrt, pi, sin, cos, atan
from typing import Union

import moderngl

from ..utils.useful_functions import * #this is for easy access to rotate
from ..utils.standard_imports import *


class Matable():
    """Short for Animatable Object, a Matable is designed to hold points, which are tuples of coordinate pairs and instructions on how to connect them.
    For simple reference, point[0] will always mean an x-value of a point, and point[1] will always mean the y-value."""
    def __init__(self, *points: Union[tuple, list]): 
        temp_list = []
        for point in points:
            temp_list.append(point)
        self.points = tuple(temp_list) #tuples require less memory overall.
    
    def draw(self, ctx: moderngl.context): 
        """*VERY* important. Every Matable must override draw, as it is central to rendering in Synthesium.
        Draw takes in a moderngl context and then applies """
        pass

    #GENERAL FUNCTIONS DEALING WITH MOVEMENT
    def rotate(self, degrees, center, rotates_clockwise = True): 
        for point in self.points: 
            rotate(point, degrees, center, rotates_clockwise) #check utils.useful_functions for the whole breakdown.
            
    def shift(self, amt: tuple):
        """Shifts are done by adding a tuple of length 4, with each value corresponding to right, left, up, and down movement."""
        new_point_list = [] #temp list to hold new points
        for point in self.points: 
            new_x_value = point[0] + amt[0] - amt[1] #calculate shifted x-coord
            new_y_value = point[1] + amt[2] - amt[3] #calculate shifted y-coord
            new_point_list.append(tuple(new_x_value, new_y_value))
        self.points = tuple(new_point_list)
    
class Line(Matable) : 
    """A class made for straight lines going between two Points."""
    def __init__(self, bound1: tuple, bound2: tuple) : 
        self.bound1 = bound1
        self.bound2 = bound2
    
    #getters and setters
    def set_bound1(self, bound1) :
        self.bound1 = bound1
        
    def get_bound1(self) :
        return self.bound1
    
    def set_bound2(self, bound2) : 
        self.bound2 = bound2
        
    def get_bound2(self) : 
        return self.bound2

class Bezier(Line): 
    pass #to be implemented later
    
class Polygon(Matable) : 
    """Base class for Polygons, as the name suggests."""
    def __init__(self, *points: Union[tuple, list]): 
        super().__init__(points)
    
    def get_num_points(self) : 
        return len(self.points)
    
    def get_points(self) : 
        return self.points

    def __str__(self) : 
        string = ""
        for i, point in enumerate(self.points) : 
            string += f"{i}: {point}\n"
        return string
    
    def __repr__(self) : 
        return f"{type(self)}(*self.points)"
        
    def shift(self, amt: tuple) : 
        for point in self.points : 
            point = point.shift(amt)
        
        self = Polygon(*self.points)
        return self
       
class Quadrilateral(Polygon) :
    """Class for any Quadrilaterals, inheriting from Polygon."""
    def __init__(self, point1, point2, point3, point4) : 
        super().__init__(point1, point2, point3, point4)

class Triangle(Polygon): 
    """I would think the name is self-explanatory."""
    def __init__(self, point1, point2, point3): 
        super().__init__(point1, point2, point3)

class Circle(Matable) : 
    def __init__(self, center, radius) : 
        self.center = center
        self.radius = radius
        self.circumference = pi * (radius **2) 
    
    def shift(self, amt: tuple):
        self.center.shift(amt)


p = Matable((0,0), (0, 1), (1, 0))
print(p)