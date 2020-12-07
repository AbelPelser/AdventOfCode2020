import unittest

from puzzles.Day7.day7 import part1, part2
from test.TestConfig import TestConfig


class Day7Test(TestConfig, unittest.TestCase):
    def test_day7_part1(self):
        self.assertEqual(part1(), 378)

    def test_day7_part2(self):
        self.assertEqual(part2(), 27526)
