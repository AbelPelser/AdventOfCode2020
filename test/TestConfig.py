import os
import re
import sys
import unittest


class TestConfig(object):
    def __init__(self):
        super().__init__()
        self.day_n = int(''.join(re.findall('\\d+', self.__class__.__name__)))

    # def setUp(self) -> None:
        # sys.path.append(os.getcwd())
        # raise Exception(f'../puzzles/Day{self.day_n}')
        # os.chdir(f'../puzzles/Day{self.day_n}')
