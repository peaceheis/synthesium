from math import sqrt, pi, sin, cos, atan
from typing import Iterable

from ..utils.useful_functions import *
from ..utils.imports import * 


class Matable():
    """Short for Animatable Object, a Matable is designed to hold points, which are tuples of coordinate pairs and instructions on how to connect them.
    For simple reference, point[0] will always mean an x-value of a point, and point[1] will always mean the y-value."""
    def __init__(self, *points: Union[tuple, list]): 
        temp_list = []
        for point in points:
            temp_list.append(point)
        self.points = tuple(temp_list) #tuples require less memory space, and points generally shouldn't be changing in terms of length.
    
    def draw(self, ctx): #TODO, implement draw()
        """*VERY* important. Every Matable must override draw, as it is central to rendering in Synthesium.
        Draw takes in an empty cairo context, prints itself on it, and then returns a pixel array, but draw can ignore the cairo context and simply 
        use a pixel array."""


    #GENERAL FUNCTIONS DEALING WITH MOVEMENT
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
            point = tuple(*point)
        self.points = tuple(*self.points)
        return self
            
    def shift(self, amt: tuple):
        """Shifts are done by adding a tuple of length 4, with each value corresponding to right, left, up, and down movement."""
        new_point_list = [] #temp list to hold new points
        for point in self.points: 
            new_x_value = point[0] + amt[0] - amt[1] #calculate shifted x-coord
            new_y_value = point[1] + amt[2] - amt[3] #calculate shifted y-coord
            new_point_list.append(tuple(new_x_value, new_y_value))
        self.points = tuple(*new_point_list)
        return self

    def set_points(self, *points): 
        if len(points) == len(self.points): 
            self.points = tuple(*points)
            return self
        else: 
            raise Exception("Length of argument points was different than length of self.points")

        
        

class MatableGroup(Matable): 
    """Mostly for internal usage, a MatableGroup is just that: a group of Matables treated like a single Matable.
    Functions applied to a Matable Group will be applied as if the MatableGroup is one matable. To affect a single Matable, 
    access it with MatableGroup.matables[index]"""
    def __init__(self, *matables: Iterable): 
        self.matables = matables
    
    def rotate(self, degrees, center, rotates_clockwise=True): 
        self.matables = [matable.rotate(degrees, center, rotates_clockwise) for matable in self.matables]

    def shift(self, amt: tuple): 
        self.shift = [matable.shift(amt) for matable in self.matables]

    def draw(self): 
        for matable in self.matables: matable.draw()
        

#some predefined Matables
class Curve(Matable): 
    def __init__(self, *bounds): 
        self.bounds = {f"bound{i}":bound for i, bound in enumerate(bounds)} #TODO, enable some interesting Curve functionality

class Line(Curve) : 
    """A class made for straight lines going between two points."""
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

    
class Polygon(Matable) : 
    """Base class for Polygons, as the name suggests."""
    def __init__(self, *points): 
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
        return f"Polygon({self.points})"
        
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


class Arc(): 
    def __init__(self, center: tuple, radius: int, degrees: int): 
        self.center = center
        self.radius = radius
        self.degrees = degrees 
        
    def get_arc_length(self): 
        return self.radius*2 * (self.degrees/360) * pi #the arclength formula

    def draw(self, ctx: cairo.Context): 
        pass

    

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

    def draw(self, surface: cairo.ImageSurface, ctx): 
        width = surface.get_width()
        height = surface.get_height() 
        ctx.new_sub_path()
        ctx.set_source_rgba(1, 0, 0, 1)
        ctx.arc(*self.center, self.radius, 0, 2*pi)
        ctx.stroke()
        return surface

