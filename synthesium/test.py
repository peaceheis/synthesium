from synthesium.canvas.canvas import Canvas
from synthesium.matable.shapes import *
from synthesium.mation.colormations import ChangeRedFill, ChangeOpacity
from synthesium.mation.mationgroup import SameTargetGroup
from synthesium.mation.movemations import MovePoint
from synthesium.mation.timestamp import TimeStamp
from synthesium.utils.colors import *


class TestCanvas(Canvas):
    def construct(self):
        self.fps = 60
        self.background_color = PURE_GREEN

        rect = Curve(Point(0,0), Point(0,0), Point(0, 0), Point(0, 0))
        Move1 = MovePoint(rect, 1, (1000, 0), TimeStamp(0,0,0), TimeStamp(0,5,0))
        Move2 = MovePoint(rect, 2, (2000, 2000), TimeStamp(0,0,0), TimeStamp(0,5,0))
        Move3 = MovePoint(rect, 0, (0, 2000), TimeStamp(0, 0, 0), TimeStamp(0, 5, 0))
        self.add(SameTargetGroup(rect, Move1, Move2, Move3))


t = TestCanvas(frame_size=(2000, 2000), canvas_size=(2000, 2000))
t.write("/Users/scakolatse/coding-projects/synthesium/synthesium/tests/test.mp4")
