"""The 'primitive' classes that make up the basis of all the Matables in Synthesium: (straight) Lines, Arcs, and (cubic bezier) Curves.
Rendering in Synthesium (should) reduce everything to these. The reason for these primitives is to have a one to one match for the drawing functions
in cairo, line_to(), curve_to(), and arc(). By doing this, all other shapes can be defined as MatableGroups, which have different combinations of these primitives."""

from synthesium.utils.colors import PURE_BLUE
from math import pi

from synthesium.utils.imports import *
from synthesium.matables.matable import Matable

class Line(Matable): 
    def __init__(self, point1, point2, **kwargs):
        super().__init__(point1, point2, **kwargs)

class Arc(Matable): 
    def __init__(self, center: tuple, radius: int, degrees: int, color = PURE_BLUE): 
        self.center = center
        self.radius = radius
        self.degrees = degrees 
        self.color = color
        self.points = (center, ) #for compatability purposes with the rest of the engine, which assumes all Matables have a tuple attribute called self.points.
        
    def get_arc_length(self): 
        return self.radius*2 * (self.degrees/360) * pi #the arclength formula

class Curve(Matable):
    def __init__(self, anchor1, handle1, handle2, anchor2): 
        self.points = (anchor1, handle1, handle2, anchor2) #look into bezier curves, namely cubic ones, for info on how this works.
