"""The 'primitive' classes that make up the basis of all the Matables in Synthesium: (straight) Lines, Arcs, and (cubic bezier) Curves.
Rendering in Synthesium (should) reduce everything to these. The reason for these primitives is to have a one to one match for the drawing functions
in cairo, line_to(), curve_to(), and arc(). By doing this, all other shapes can be defined as MatableGroups, which have different combinations of these primitives."""

from synthesium.utils.colors import PURE_BLUE
from math import pi

from synthesium.utils.imports import *
from synthesium.matable.matable import Matable

class Line(Matable): 
    def __init__(self, point1, point2, **kwargs):
        super().__init__(point1, point2, **kwargs)

    def get_point1(self): 
        return self.points[0]

    def set_point1(self, point):
        self.points[0] = point
        return self

    def get_point2(self):
        return self.points[1]

    def set_point2(self, point):
        self.point[1] = point
        return self

class Arc(Matable): 
    def __init__(self, center: tuple, radius: int, angle1: int, angle2: int, **kwargs): 
        default_config = {
            "color": PURE_BLUE #TODO, get rid of the config system. No. Just no.
        }
        self.center = center
        self.radius = radius
        self.angle1 = angle1
        self.angle2 = angle2 
        self.points = (center, ) #for compatability purposes with the rest of the engine, which assumes all Matables have a tuple attribute called self.points.
        self.config = self.configure(default_config, **kwargs)
        
    def arc_length(self): 
        return self.radius*2 * (self.degrees/360) * pi #the arclength formula

    @property
    def center(self):
        return self.center

    @center.setter
    def set_center(self, center): 
        self.center = center
        self.points = (center, )
        return self

    @property
    def radius(self): 
        return self.radius

    @radius.setter
    def set_radius(self, radius): 
        self.radius = radius

    def degrees(self): 
        return abs(self.angle1 - self.angle2)
    
    @property
    def angle1(self): 
        return self.angle1

    @angle1.setter
    def set_angle1(self, angle): 
        self.angle1 = angle
        return self

    @property
    def angle2(self): 
        return self.angle2

    @property.setter
    def set_angle2(self, angle): 
        self.angle2 = angle
        return self


class Curve(Matable):
    def __init__(self, anchor1, handle1, handle2, anchor2): 
        self.points = (anchor1, handle1, handle2, anchor2) #look into bezier curves, namely cubic ones, for info on how this works.
