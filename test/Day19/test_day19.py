import unittest

from puzzles.Day19.day19 import part1, part2
from test.TestConfig import TestConfig


class Day19Test(TestConfig, unittest.TestCase):
    def test_day19_part1(self):
        self.assertEqual(part1(), 224)

    def test_day19_part2(self):
        self.assertEqual(part2(), 436)
