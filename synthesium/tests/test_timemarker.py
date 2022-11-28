import unittest

from synthesium.mutator import timestamp
from synthesium.mutator.timestamp import TimeStamp


class TimeStampTest(unittest.TestCase):
    def setUp(self) -> None:
        self.less = TimeStamp(1, 3, 2)
        self.more = TimeStamp(3, 0, 4)
        self.base = TimeStamp(2, 2, 1)
        self.incrementer = TimeStamp()
        self.test_fps = 30
        timestamp.FPS = self.test_fps

    def test_incrementer(self):
        for _ in range(self.test_fps * 60):
            self.incrementer.increment()

        self.assertEqual(TimeStamp(1, 0, 0), self.incrementer)

    def test_lt(self):
        self.assertLess(self.less, self.base, msg="Less not < Base")

    def test_gt(self):
        self.assertGreater(self.more, self.base, msg="More not > Base")

    def test_eq(self):
        self.assertEqual(self.base, self.base, msg="Base not == Base")

    def test_leq(self):
        self.assertLessEqual(self.less, self.base, msg="Less not <= Base")

    def test_geq(self):
        self.assertGreaterEqual(self.more, self.base, msg="More not >= Base")

    def test_not_gt(self):
        self.assertIsNot(self.base, self.base > self.base, msg="Base > Base")

    def test_not_leq(self):
        self.assertIsNot(self.base, self.base <= self.less, msg="Base <= Less")
