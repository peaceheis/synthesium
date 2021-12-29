from synthesium.mation.timemarker import TimeMarker
from synthesium.canvas.canvas import Canvas
from synthesium.mation.mation import Mation
from synthesium.mation.mations import Move, Show
from synthesium.matable.shapes import *
from synthesium.utils.useful_functions import *

class TestCanvas(Canvas): 
    def construct(self):
        self.fps = 24
        circle = Circle( Point(300, 300), 200)
        triangle = Triangle( Point(0, 0), Point(500, 500), Point(300, 300))
        move = Move(circle, (300, 0, 300, 0), TimeMarker(0,0), TimeMarker(0, 1, 24))
        show2 = Show(triangle, TimeMarker(0,0,0), TimeMarker(0,4,3), rate_func = constant)
        self.add(show2)
        
t = TestCanvas()
t.write("/Users/scakolatse/coding-projects/synthesium/synthesium/tests/test.mp4")



