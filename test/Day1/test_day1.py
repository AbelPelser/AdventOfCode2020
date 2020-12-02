import unittest

from puzzles.Day1.day1 import part1, part2
from puzzles.Day1.day1_z3 import part1_z3, part2_z3
from test.TestConfig import TestConfig


class Day1Test(TestConfig, unittest.TestCase):

    def test_part1(self):
        self.assertEqual(part1(), 1016131)

    def test_part2(self):
        self.assertEqual(part2(), 276432018)

    def test_part1_z3(self):
        self.assertEqual(part1_z3(), 1016131)

    def test_part2_z3(self):
        self.assertEqual(part2_z3(), 276432018)
