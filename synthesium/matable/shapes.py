"""Predefined Matables made of the Primitives Line, Arc, and Curve"""
from typing import Union

from synthesium.matable.matablegroup import MatableGroup
from synthesium.matable.primitives import *  # Arc, Line, Curve


class Circle(Arc):
    """Circles are really just 360 degree Arcs."""

    def __init__(self, center: Point, radius: int, **kwargs):
        super().__init__(center, radius, 0, 360, **kwargs)
        self.circumference = pi * (radius ** 2)

    def shift(self, amt: tuple):
        center: Point = self.center
        new_x_value = center.x + amt[0]
        new_y_value = center.y + amt[1]
        self.center = Point(new_x_value, new_y_value)
        return self

    def get_center(self) -> Point:
        return self.center

    def set_center(self, center: Point):
        self.center = center
        return self

    def get_radius(self) -> Union[int, float]:
        return self.radius

    def set_radius(self, radius: Union[int, float]):
        self.radius = radius
        return self

    def __repr__(self):
        return f"Circle({self.center}, {self.radius})"


# slightly more involved geometry goes here.
class Polygon(MatableGroup):
    """Base class for Polygons, as the name suggests. Most of its functionality lies in being able to converting points to Lines to direct to the
       MatableGroup constructor."""

    def __init__(self, *points, **kwargs):
        default_config = {
            "line_width": 10,
            "color": PURE_RED,
            "fill_color": PURE_GREEN
        }

        matables = []
        for i in range(
                len(points) - 1):  # using 1 less because the last point has to connect to the first point, which requires special handling.
            matables.append(Line(points[i], points[i + 1]))
        matables.append(Line(points[-1], points[0]))  # connect last element and first element.

        super().__init__(*matables, **kwargs)  # let MatableGroup handle the rest.
        self.configure(default_config,
                       **kwargs)  # while MatableGroup also has configure() in the init, it's best to update with Polygon's default config.

    def __repr__(self):
        return f"Polygon({self.points})"


class Quadrilateral(Polygon):
    """Class for any Quadrilaterals, inheriting from Polygon. """

    def __init__(self, point1, point2, point3, point4, **kwargs):
        """Instead of making the user create each individual Matable, all the user has to do is give the points and Synthesium generates the rest."""
        super().__init__(point1, point2, point3, point4, **kwargs)


class Square(Polygon):
    """A class that enforces all the side lengths to be the same."""

    def __init__(self, center, side_length, **kwargs):
        """[to make sure that a square is generated, the center and side length are given, and the points are generated by 
            going out half the side length in the +x +y, +x, -y, -x, -y, and -x, +y directions.]

        Args:
            center ([tuple]): [the x and y coordinates of the center.]
            side_length ([Union[float, int]]): [the length of the sides (obviously)]
        """
        half_side_length = side_length / 2
        points = [
            center[0] + half_side_length, center[1] + half_side_length,  # positive x and y
            center[0] - half_side_length, center[0] + half_side_length,  # negative x, positive y
            center[0] - half_side_length, center[0] - half_side_length,  # negative x and y
            center[0] + half_side_length, center[0] - half_side_length,  # positive x and negative y
        ]

        super().__init__(*points, **kwargs)


class Triangle(Polygon):
    """I would think the name is self-explanatory."""

    def __init__(self, point1, point2, point3, **kwargs):
        super().__init__(point1, point2, point3, **kwargs)
