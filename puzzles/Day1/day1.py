import itertools

from util import mult, read_input_as_numbers


def find_sum_combo(numbers, n, target=2020):
    for perm in itertools.combinations(numbers, n):
        if sum(perm) == target:
            return mult(perm)


def part1():
    return find_sum_combo(read_input_as_numbers(), 2)


def part2():
    return find_sum_combo(read_input_as_numbers(), 3)


if __name__ == '__main__':
    print(part1())
    print(part2())
