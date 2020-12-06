import unittest

from puzzles.Day5.day5 import part1, part2
from test.TestConfig import TestConfig


class Day5Test(TestConfig, unittest.TestCase):
    def test_day5_part1(self):
        self.assertEqual(part1(), 944)

    def test_day5_part2(self):
        self.assertEqual(part2(), 554)
