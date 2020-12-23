import unittest

from puzzles.Day14.day14 import part1, part2
from test.TestConfig import TestConfig


class Day14Test(TestConfig, unittest.TestCase):
    def test_day14_part1(self):
        self.assertEqual(part1(), 4297467072083)

    def test_day14_part2(self):
        self.assertEqual(part2(), 5030603328768)
