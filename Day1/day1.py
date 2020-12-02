import itertools

from util import mult, read_input_as_numbers, time_call


def find_sum_combo(numbers, n, target=2020):
    for perm in itertools.combinations(numbers, n):
        if sum(perm) == target:
            return mult(perm)


def part1(numbers, target=2020):
    return find_sum_combo(numbers, 2, target=target)


def part2(numbers, target=2020):
    return find_sum_combo(numbers, 3, target=target)


if __name__ == '__main__':
    input_numbers = read_input_as_numbers()
    time_call(part1, input_numbers)
    time_call(part2, input_numbers)
