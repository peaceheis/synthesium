"""The 'primitive' classes that make up the basis of all the Matables in Synthesium: (straight) Lines, Arcs, and (cubic bezier) Curves.
Rendering in Synthesium (should) reduce everything to these. The reason for these primitives is to have a one to one match for the drawing functions
in cairo, line_to(), curve_to(), and arc(). By doing this, all other shapes can be defined as MatableGroups, which have different combinations of these primitives."""

from math import pi

from synthesium.matable.matable import Matable
from synthesium.matable.point import Point
from synthesium.utils.colors import PURE_BLUE, HALF_OPAQUE_RED


class Line(Matable):
    def __init__(self, point1: Point, point2: Point, **kwargs):
        super().__init__(point1, point2, **kwargs)

    def get_point1(self):
        return self.points[0]

    def set_point1(self, point: Point):
        self.points.x = point
        return self

    def get_point2(self):
        return self.points[1]

    def set_point2(self, point: Point):
        self.point.y = point
        return self


class Arc(Matable):
    def __init__(self, center: Point, radius: int, angle1: int, angle2: int, negative=False, **kwargs):
        default_config = {
            "color": PURE_BLUE,
            "fill_color": HALF_OPAQUE_RED,
            "line_width": 10
        }
        self.center = center
        self.radius = radius
        self.angle1 = angle1
        self.angle2 = angle2
        self.points = center,
        # for compatability purposes with the rest of the library, which assumes all Matables have a tuple attribute called self.points.
        self.negative = negative
        self.config = self.configure(default_config, **kwargs)
        self.degrees = abs(angle1 - angle2)

    def arc_length(self) -> float:
        return self.radius * 2 * (self.degrees / 360) * pi  # the arc length formula

    def get_center(self) -> Point:
        return self.center

    def set_center(self, center: Point):
        self.center = center
        self.points = center,
        return self

    def get_radius(self):
        return self.radius

    def set_radius(self, radius: Point):
        self.radius = radius

    def get_degrees(self):
        return abs(self.angle1 - self.angle2)

    def get_angle1(self):
        return self.angle1

    def set_angle1(self, angle: int):
        self.angle1 = angle
        return self

    def get_angle2(self):
        return self.angle2

    def set_angle2(self, angle: int):
        self.angle2 = angle
        return self


class Curve(Matable):
    def __init__(self, anchor1: Point, handle1: Point, handle2: Point, anchor2: Point):
        self.points = (anchor1, handle1, handle2, anchor2)  # look into Bézier curves, namely cubic ones, for info on how this works.
