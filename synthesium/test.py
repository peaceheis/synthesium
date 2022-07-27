from synthesium.canvas.canvas import Canvas
from synthesium.matable.shapes import *
from synthesium.mation.colormations import ChangeBlueFill, ChangeGreenFill, ChangeRedFill
from synthesium.mation.mationgroup import SameTargetGroup
from synthesium.mation.movemations import Transform
from synthesium.mation.timestamp import TimeStamp
from synthesium.utils.useful_functions import *
from synthesium.utils.colors import *


class TestCanvas(Canvas):
    def construct(self):
        self.fps = 24
        self.background_color = BLACK

        circle = Circle(Point(500, 500), 0, color=[0, 0, 0, 0])

        MoveCircle = Transform(circle, "radius", 500, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0))
        MoveCircle2 = Transform(circle, "radius", 0, TimeStamp(0, 3, 1), TimeStamp(0, 6, 0))
        blue = ChangeBlueFill(circle, 1, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0))
        red = ChangeRedFill(circle, 1, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0))
        green = ChangeGreenFill(circle, 1, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0))
        blue2 = ChangeBlueFill(circle, 0, TimeStamp(0, 3, 1), TimeStamp(0, 6, 0))
        red2 = ChangeRedFill(circle, 0, TimeStamp(0, 3, 1), TimeStamp(0, 6, 0))
        green2 = ChangeGreenFill(circle, 0, TimeStamp(0, 3, 1), TimeStamp(0, 6, 0))

        self.add(SameTargetGroup(circle, MoveCircle, blue, red, green),
                 SameTargetGroup(circle, MoveCircle2, blue2, red2, green2))


t = TestCanvas(frame_size=(2000, 2000), canvas_size=(2000, 2000))
t.write("/Users/scakolatse/coding-projects/synthesium/synthesium/tests/test.mp4")
