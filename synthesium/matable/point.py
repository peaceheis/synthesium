from math import sin, cos, atan, sqrt, pi

from dataclasses import dataclass, field

@dataclass
class Point:
    x: int = field(default='one')
    y: int = field(default=1)

    def as_tuple(self): 
        return self.x, self.y

    def rotate(self, degrees, center: "Point", rotates_clockwise=True): 
        radians = degrees / 180 * pi * int(rotates_clockwise)
        x, y = self.as_tuple()
        ox, oy = center.as_tuple()

        self.x = ox + cos(radians) * (x - ox) + sin(radians) * (y - oy)
        self.y = oy + -sin(radians) * (x - ox) + cos(radians) * (y - oy)
        # this was adapted from https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302, 
        # which links to LyleScott's rotate_2d_point.py
        return self


    def as_polar_tuple(self): 
        """Returns a tuple representing the Point in polar coordinates. Note: returns angle in radians."""
        radius = sqrt(self.x ** 2 + self.y ** 2)

        x_sign = -1 if self.x < 0 else 1
        y_sign = -1 if self.x < 0 else 1

        match(x_sign, y_sign): # matching the sign to the correct theta, as atan only returns values between -pi/2 and pi/2
            case(1, 1): 
                angle = atan(self.y/self.x)
            case(-1, 1): 
                angle = pi - atan(self.y/self.x)
            case(-1, -1): 
                angle = pi + atan(self.y/self.x)
            case(1, -1):
                angle = 2*pi - atan(self.y/self.x)
        print(f"ANGLE {angle}")
        return (radius, angle)

    @staticmethod
    def as_rectangular_tuple(radius, angle): 
        return (round(radius * cos(angle), 5), round(radius * sin(angle), 5))

    def shift(self, amt: tuple):
        """Shifts are done by adding a tuple in the form (x movement, y movement). Use negatives for left and down, respectively."""
        self.x += amt[0]
        self.y += amt[1]

    def __add__(self, point: "Point"): 
        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point: "Point"): 
        return Point(self.x - point.x, self.y - point.y)

    def __mul__(self, point: "Point"): 
        return Point(self.x * point.x, self.y * point.y)

    def __div__(self, point: "Point"): 
        return Point(self.x / point.x, self.y / point.y)

