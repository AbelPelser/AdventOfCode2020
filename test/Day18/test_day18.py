import unittest

from puzzles.Day18.day18 import part1, part2
from test.TestConfig import TestConfig


class Day18Test(TestConfig, unittest.TestCase):
    def test_day18_part1(self):
        self.assertEqual(part1(), 21993583522852)

    def test_day18_part2(self):
        self.assertEqual(part2(), 122438593522757)
