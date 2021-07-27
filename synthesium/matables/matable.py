from math import sqrt, pi, sin, cos, atan
from typing import Iterable

from synthesium.utils.useful_functions import *
from synthesium.utils.imports import * 

class Matable(): 
    """Short for Animatable Object, a Matable is designed to hold points, which are tuples of coordinate pairs and instructions on how to connect them.
    For simple reference, point[0] will always mean an x-value of a point, and point[1] will always mean the y-value."""
    def __init__(self, *points: "Union[tuple[tuple], list[tuple]]", **kwargs: "dict[str, Any]"): 
        default_config = {
            "color": PURE_BLUE,
            "fill_color": PURE_BLUE,
        } 

        self.points = tuple(points) #tuples require less memory space, and points generally shouldn't be changing in terms of length.
        self.config = self.configure(default_config, **kwargs)

    def configure(self, default_config, **kwargs): 
        """Configure works by taking in all the kwargs passed to init(), and comparing them against the default config. Anything new is updated, 
           otherwise the defaults are used. This allows for the dynamic setting of attributes in one dictionary."""
        new_config = kwargs
        for key, value in new_config.items(): default_config[key] = value #update the default_config as necessary with new values
        return default_config #while it returns "default_config," it's really returning the modified config. 
        

    #movement functions
    def rotate(self, degrees, center, rotates_clockwise = True): 
        """
        A bit confusing, but rotate uses math to calculate the rotation of a Point around another (henceforth the Anchor).
        This is achieved by first setting the Anchor as the "origin" by changing the point's coords
        to the relative x + y distance to the Anchor,
        Then converting from Rectangular to Polar coordinates; they are designed to be good for rotation.
        After adding the desired degrees to the Polar coordinates,
        We convert back to Rectangular coordinates,
        And shift back so that the origin is the origin, not the Anchor.
        """
        from math import sin, cos, atan, pi
        self.points = list(*self.points)

        for point in self.points: 
            point = list(*point)
            #set Anchor to be origin 
            point[0] -= center[0]
            point[1] -= center[1]

            #generating polar coordinates
            radius = sqrt(point[0]**2 + point[1]**2)
            try : 
                angle = atan(point[1] / point[0])
            except :
                #prevent errors from being thrown if x == 0 
                if abs(point[1]) == point[1] : 
                    angle = pi / 2
                else : 
                    angle = 3 * pi / 2

            #rotates by adding the angle (in radians)
            radians = pi * degrees / 180
            if rotates_clockwise : 
                angle -= radians
            else :     
                angle += radians

            #convert back to rectangular coordinates
            point[0] = round(radius * cos(angle), 5)
            point[1] = round(radius * sin(angle), 5) 

            #shift back from center being origin to original location
            point[0] += center[0]
            point[1] += center[1]
            point = tuple(point)
        self.points = tuple(self.points)
        return self
            
    def shift(self, amt: tuple):
        """Shifts are done by adding a tuple of length 4, with each value corresponding to right, left, up, and down movement."""
        new_point_list = [] #temp list to hold new points
        for point in self.points: 
            new_x_value = point[0] + amt[0] - amt[1] #calculate shifted x-coord
            new_y_value = point[1] + amt[2] - amt[3] #calculate shifted y-coord
            new_point_list.append((new_x_value, new_y_value))
        self.points = tuple(new_point_list)
        return self

    #Getters and setters
    def set_points(self, *points): 
        self.points = tuple(points)

    def get_points(self): 
        return self.points

    def get_num_points(self): 
        return len(self.points)

    def __repr__(self): 
        return f"Matable of type {self.__class__.__name__} consisting of points {self.points}" #TODO, make better REPR
        
    def __str__(self): 
        return f"Matable of type {self.__class__.__name__} consisting of points {self.points}"    