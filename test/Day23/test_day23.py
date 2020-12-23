import unittest

from puzzles.Day23.day23 import part1, part2
from test.TestConfig import TestConfig


class Day23Test(TestConfig, unittest.TestCase):
    def test_day23_part1(self):
        self.assertEqual(part1(), '28946753')

    def test_day23_part2(self):
        self.assertEqual(part2(), 519044017360)
