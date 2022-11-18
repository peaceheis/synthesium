import unittest

from synthesium.mutator.timestamp import TimeStamp


class TimeStampTest(unittest.TestCase):
    def setUp(self) -> None:
        self.less = TimeStamp(1, 3, 2)
        self.more = TimeStamp(2, 2, 4)
        self.base = TimeStamp(2, 0, 1)

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
