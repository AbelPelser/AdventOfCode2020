from typing import List, Set

from util import read_input_as_numbers


def find_unsummed_nr(numbers: List[int], past_n_to_check: int):
    sums_with_previous: List[Set[int]] = [set() for _ in range(len(numbers))]
    for i in range(len(numbers)):
        from_i = max(0, i - past_n_to_check)
        for j in range(from_i, i):
            sums_with_previous[i].add(numbers[i] + numbers[j])
        if i >= past_n_to_check:
            if not any(numbers[i] in sums_with_previous[j] for j in range(from_i, i)):
                return numbers[i]
    raise ValueError("No suitable number found")


def find_summing_sequence(numbers: List[int], n):
    start, end = 0, 1
    while end < len(numbers):
        seq = numbers[start:end]
        seq_sum = sum(seq)
        if seq_sum == n:
            return seq
        elif seq_sum < n:
            end += 1
        else:
            start += 1
    raise ValueError("No suitable sequence found")


def part1():
    return find_unsummed_nr(read_input_as_numbers(), 25)


def part2(desired_sum=18272118):
    seq = find_summing_sequence(read_input_as_numbers(), desired_sum)
    return min(seq) + max(seq)


if __name__ == '__main__':
    print(part1())
    print(part2())
