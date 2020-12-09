import unittest

from puzzles.Day8.day8 import part1, part2
from test.TestConfig import TestConfig


class Day8Test(TestConfig, unittest.TestCase):
    def test_day8_part1(self):
        self.assertEqual(part1(), 1832)

    def test_day8_part2(self):
        self.assertEqual(part2(), 662)
