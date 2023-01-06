import cProfile

from synthesium.canvas.canvas import Canvas
from synthesium.mutator.timestamp import TimeStamp
from synthesium.tests.TestEntity import TestEntity


class Demonstration(Canvas):
    def construct(self):
        test = TestEntity(1000, 1000, 0xFFFFFFFF)
        # transformation = Transform(circle, "radius", 25, TimeStamp(0, 0, 0), TimeStamp(0, 3, 0))
        self.entities.append(test)
        test.add_visibility_window((TimeStamp(0, 0, 0), TimeStamp(0, 1, 23)))


cProfile.run(
    'Demonstration("/Users/scakolatse/coding-projects/synthesium/demonstration.mp4", 1000, 1000)',
    "stats",
)
