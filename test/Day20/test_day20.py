import unittest

from puzzles.Day20.day20 import part1, part2
from test.TestConfig import TestConfig


class Day20Test(TestConfig, unittest.TestCase):
    def test_day20_part1(self):
        self.assertEqual(part1(), 27803643063307)

    def test_day20_part2(self):
        self.assertEqual(part2(), 1644)
