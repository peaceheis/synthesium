from synthesium.mation.timestamp import TimeStamp
from synthesium.canvas.canvas import Canvas
from synthesium.mation.mations import Transform
from synthesium.matable.shapes import *
from synthesium.utils.useful_functions import *

class TestCanvas(Canvas): 
    def construct(self):
        self.fps = 24
        arc = Arc(Point(350, 350), 0, 0, 2*pi)
        #self.add(Transform(arc, "radius", 50, TimeStamp(0,0,0),TimeStamp(0,3,0)))
        #self.add(Transform(arc, "radius", 0, TimeStamp(0,3,1),TimeStamp(0,6,0)))

        self.add(Transform(Arc(Point(700, 700), 250, 0, 0), "angle2", pi, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0)))
        self.add(Transform(Arc(Point(700, 700), 250, 0, 0, negative=True), "angle2", -pi, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0)))
        
t = TestCanvas()
t.write("/Users/scakolatse/coding-projects/synthesium/synthesium/tests/test.mp4")



