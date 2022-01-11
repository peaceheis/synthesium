from synthesium.mation.mationgroup import MationGroup
from synthesium.mation.sametargetgroup import SameTargetGroup
from synthesium.mation.timestamp import TimeStamp
from synthesium.canvas.canvas import Canvas
from synthesium.mation.mations import MovePoint, Show, Transform, Rotate
from synthesium.matable.shapes import *
from synthesium.utils.useful_functions import *

class TestCanvas(Canvas): 
    def construct(self):
        self.fps = 60
        self.background_color = BLACK
        circle = Circle(Point(500,500), 0, color=WHITE)
        self.add(Transform(circle, "radius", 500, TimeStamp(0,0,0), TimeStamp(0,3,0), rate_func=linear_decrease))
        self.add(Transform(circle, "radius", 0, TimeStamp(0,3,1), TimeStamp(0,6,0), rate_func=linear_increase))

t = TestCanvas(frame_size=(1000,1000), canvas_size=(1000,1000))
t.write("/Users/scakolatse/coding-projects/synthesium/synthesium/tests/test.mp4")



