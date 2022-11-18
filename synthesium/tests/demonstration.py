from synthesium.canvas.canvas import *
from synthesium.entity.point import Point
from synthesium.entity.shapes import Circle
from synthesium.mutator.motionmutators import Transform
from synthesium.mutator.timestamp import TimeStamp


class Demonstration(Canvas):
    def construct(self):
        for i in range(10):
            circle = Circle(Point(10 + i * 50, 10 + i * 50), 0)
            transformation = Transform(circle, "radius", 25, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0))
            self.add(transformation)


d = Demonstration()

d.write("/Users/scakolatse/coding-projects/synthesium/demonstration.mp4")
