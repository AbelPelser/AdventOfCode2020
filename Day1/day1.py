import itertools
import time
from functools import reduce

from util import mult, read_input


def find_sum_combo(numbers, n, target=2020):
    for perm in itertools.combinations(numbers, n):
        if sum(perm) == target:
            return mult(perm)


def part1(numbers, target=2020):
    return find_sum_combo(numbers, 2)


def part2(numbers, target=2020):
    return find_sum_combo(numbers, 3)


if __name__ == '__main__':
    text = read_input()
    t1 = time.time()
    print(part1(text))
    print(part2(text))
    print(f'Time taken: {time.time() - t1}')
