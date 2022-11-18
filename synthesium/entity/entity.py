from synthesium.entity.point import Point
from synthesium.utils.colors import PURE_BLUE


class Entity:
    """An is designed to hold points,
    which are named tuples of coordinate pairs, and instructions on how to connect them.\n
    For simple reference, both point.x and point.x will mean the x-value of a point, and point.y/point.y means the y-value."""

    def __init__(self, *points: "Union[tuple[Point], list[Point]]", color_stops=None, **kwargs: "dict[str, Any]"):
        if color_stops is None:
            color_stops = []
        self.config = {
            "color": PURE_BLUE,
            "fill_color": PURE_BLUE,
            "line_width": 10
        }

        self.points = tuple(
            points)  # tuples require less memory space, and points generally shouldn't be changing in terms of length.
        self.color_stops = color_stops
        self.config = self.configure(self.config, **kwargs)

    def configure(self, default_config, **kwargs):
        """Configure works by taking in all the kwargs passed to init(), and comparing them against the default config. Anything new is updated, 
           otherwise the defaults are used. This allows for the dynamic setting of attributes in one dictionary."""
        new_config = kwargs
        for key, value in new_config.items(): default_config[
            key] = value  # update the default_config as necessary with new values
        return default_config  # while it returns "default_config," it's really returning the modified config.

    # movement functions
    def rotate(self, degrees, center: Point, rotates_clockwise=True):
        for point in self.points:
            point.rotate(degrees, center, rotates_clockwise)

    def shift(self, amt: tuple):
        """Shifts are done by adding a tuple of length 2, in the form (x movement, y movement). Use negatives for
        left and down, respectively.

        Args:
            amt: tuple of length 2 in the form (x movement, y movement)"""
        self.points = tuple([point.shift(amt) for point in self.points])
        return self

    # properties
    def get_points(self):
        """

        Returns:
            object:
        """
        return self.points

    def set_points(self, *points):
        self.points = tuple(points)
        return self

    def num_points(self):
        return len(self.points)

    def set_red(self, val):
        assert 0 <= val <= 1
        self.config["color"][0] = val

    def set_red_fill(self, val):
        assert 0 <= val <= 1
        self.config["fill_color"][0] = val

    def get_red(self):
        return self.config["color"][0]

    def get_red_fill(self):
        return self.config["fill_color"][0]

    def set_green(self, val):
        assert 0 <= val <= 1
        self.config["color"][1] = val

    def set_green_fill(self, val):
        assert 0 <= val <= 1
        self.config["fill_color"][1] = val

    def get_green(self):
        return self.config["color"][1]

    def get_green_fill(self):
        return self.config["fill_color"][1]

    def set_blue(self, val):
        assert 0 <= val <= 1
        self.config["color"][2] = val

    def set_blue_fill(self, val):
        assert 0 <= val <= 1
        self.config["fill_color"][2] = val

    def get_blue(self):
        return self.config["color"][2]

    def get_blue_fill(self):
        return self.config["fill_color"][2]

    def set_opacity(self, val):
        assert 0 <= val <= 1
        self.config["color"][3] = val

    def set_opacity_fill(self, val):
        assert 0 <= val <= 1
        self.config["fill_color"][3] = val

    def get_opacity(self):
        return self.config["color"][3]

    def get_opacity_fill(self):
        return self.config["fill_color"][3]

    def get_color(self):
        return self.config["color"]

    def get_color_fill(self):
        return self.config["fill_color"]

    def set_color(self, *color: "tuple | list"):
        assert len(color) == 4
        for color_ in color:
            assert 0 <= color_ <= 1

        self.config["color"] = list(color)

    def set_fill_color(self, *color: "tuple | list"):
        assert len(color) == 4
        for color_ in color:
            assert 0 <= color_ <= 1

        self.config["color"] = list(color)

    def __repr__(self):
        return f"Entity of type {self.__class__.__name__} consisting of points {self.points}"  # TODO, make better REPR

    def __str__(self):
        return f"Entity of type {self.__class__.__name__} consisting of points {self.points}"
