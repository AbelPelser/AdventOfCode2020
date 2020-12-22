import unittest

from puzzles.Day11.day11 import part1, part2
from test.TestConfig import TestConfig


class Day11Test(TestConfig, unittest.TestCase):
    def test_day11_part1(self):
        self.assertEqual(part1(), 2283)

    def test_day11_part2(self):
        self.assertEqual(part2(), 2054)
