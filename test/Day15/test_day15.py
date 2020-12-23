import unittest

from puzzles.Day15.day15 import part1, part2
from test.TestConfig import TestConfig


class Day15Test(TestConfig, unittest.TestCase):
    def test_day15_part1(self):
        self.assertEqual(part1(), 496)

    def test_day15_part2(self):
        self.assertEqual(part2(), 883)
