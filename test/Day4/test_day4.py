import unittest

from puzzles.Day4.day4 import part1, part2
from test.TestConfig import TestConfig


class Day4Test(TestConfig, unittest.TestCase):
    def test_day4_part1(self):
        self.assertEqual(part1(), 260)

    def test_day4_part2(self):
        self.assertEqual(part2(), 153)
