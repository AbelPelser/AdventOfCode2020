import unittest

from puzzles.Day17.day17 import part1, part2
from test.TestConfig import TestConfig


class Day17Test(TestConfig, unittest.TestCase):
    def test_day17_part1(self):
        self.assertEqual(part1(), 315)

    def test_day17_part2(self):
        self.assertEqual(part2(), 1520)
