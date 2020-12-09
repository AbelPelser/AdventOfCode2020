import unittest

from puzzles.Day9.day9 import part1, part2
from test.TestConfig import TestConfig


class Day9Test(TestConfig, unittest.TestCase):
    def test_day9_part1(self):
        self.assertEqual(part1(), 18272118)

    def test_day9_part2(self):
        self.assertEqual(part2(), 2186361)
