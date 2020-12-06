import unittest

from puzzles.Day6.day6 import part1, part2
from test.TestConfig import TestConfig


class Day6Test(TestConfig, unittest.TestCase):
    def test_day6_part1(self):
        self.assertEqual(part1(), 7110)

    def test_day6_part2(self):
        self.assertEqual(part2(), 3628)
