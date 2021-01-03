import unittest

from puzzles.Day25.day25 import part1
from test.TestConfig import TestConfig


class Day25Test(TestConfig, unittest.TestCase):
    def test_day25_part1(self):
        self.assertEqual(part1(), 2947148)

    def test_day25_part2(self):
        self.assertTrue(True)
