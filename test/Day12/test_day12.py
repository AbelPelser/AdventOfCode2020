import unittest

from puzzles.Day12.day12 import part1, part2
from test.TestConfig import TestConfig


class Day12Test(TestConfig, unittest.TestCase):
    def test_day12_part1(self):
        self.assertEqual(part1(), 1601)

    def test_day12_part2(self):
        self.assertEqual(part2(), 13340)
