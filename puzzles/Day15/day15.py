from collections import defaultdict

from util import read_input, safe_split


def pleasure_the_elves(puzzle_input, nth_number):
    turns_per_number = defaultdict(list)
    last_spoken = 0

    for turn, n in enumerate(puzzle_input):
        turns_per_number[n].append(turn)
        last_spoken = n

    for turn in range(len(puzzle_input), nth_number):
        if len(turns_per_number[last_spoken]) == 1:
            n = 0
        else:
            n = turns_per_number[last_spoken][-1] - turns_per_number[last_spoken][-2]
        turns_per_number[n].append(turn)
        last_spoken = n
    return last_spoken


def parse_input():
    return list(map(int, safe_split(read_input(), ',')))


def part1():
    return pleasure_the_elves(parse_input(), 2020)


def part2():
    return pleasure_the_elves(parse_input(), 30000000)


if __name__ == '__main__':
    print(part1())
    print(part2())
