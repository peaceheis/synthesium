from math import sqrt

from numpy import true_divide

from synthesium.utils.useful_functions import *
from synthesium.utils.imports import * 
from synthesium.matable.point import Point

class Matable(): 
    """Short for Animatable Object, a Matable is designed to hold points, 
    which are named tuples of coordinate pairs, and instructions on how to connect them.
    For simple reference, both point.x and point.x will mean the x-value of a point, and point.y/point.y means the y-value."""
    def __init__(self, *points: "Union[tuple[Point], list[Point]]", color_stops = [], **kwargs: "dict[str, Any]"): 
        config = {
            "color": PURE_BLUE,
            "fill_color": PURE_BLUE,
            "line_width": 10
        } 

        self.points = tuple(points) #tuples require less memory space, and points generally shouldn't be changing in terms of length.
        self.color_stops = color_stops
        self.config = self.configure(config, **kwargs)

    def configure(self, default_config, **kwargs): 
        """Configure works by taking in all the kwargs passed to init(), and comparing them against the default config. Anything new is updated, 
           otherwise the defaults are used. This allows for the dynamic setting of attributes in one dictionary."""
        new_config = kwargs
        for key, value in new_config.items(): default_config[key] = value # update the default_config as necessary with new values
        return default_config # while it returns "default_config," it's really returning the modified config. 
        

    # movement functions
    def rotate(self, degrees, center: Point, rotates_clockwise = True): 
        for point in self.points: 
            point.rotate(degrees, center, rotates_clockwise)
            
    def shift(self, amt: tuple):
        """Shifts are done by adding a tuple of length 2, in the form (x movement, y movement). Use negatives for left and down, respectively."""
        self.points = tuple([point.shift(amt) for point in self.points])
        return self

    # properties
    def get_points(self): 
        return self.points

    def set_points(self, *points): 
        self.points = tuple(points)
        return self
    
    def num_points(self): 
        return len(self.points)

    def get_color(self): 
        return self.config["color"]

    def set_color(self, color: "tuple | list"): 
        assert len(color) == 4
        for color_ in color: 
            assert 0 < color_ and color_ < 1

        self.color = color

    def __repr__(self): 
        return f"Matable of type {self.__class__.__name__} consisting of points {self.points}" #TODO, make better REPR
        
    def __str__(self): 
        return f"Matable of type {self.__class__.__name__} consisting of points {self.points}"    