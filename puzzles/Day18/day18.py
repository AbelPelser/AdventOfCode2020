import re

from util import read_input_as_lines


class FakeInt(object):
    def __init__(self, value: int):
        self.value = value

    def __add__(self, other):
        return FakeInt(self.value * other.value)

    def __mul__(self, other):
        return FakeInt(self.value + other.value)


def find_closing_bracket(s, opening_bracket_i):
    bracket_n = 0
    for i, c in enumerate(list(s)[opening_bracket_i:]):
        if c == '(':
            bracket_n += 1
        elif c == ')':
            bracket_n -= 1
        if bracket_n == 0:
            return i + opening_bracket_i


def split_sum(s):
    sum_list = []
    index = 0
    while index < len(s):
        if s[index] == '(':
            to_index = find_closing_bracket(s, index)
            sum_list.append(s[index + 1:to_index])
            index = to_index + 1
        elif s[index] == ' ':
            index += 1
        else:
            item = s[index:].split(' ')[0]
            index += len(item)
            sum_list.append(item)
    return sum_list


def eval_term(s: str) -> int:
    return int(s) if s.isdigit() else eval_sum_part1(s)


def eval_sum_part1(s: str) -> int:
    sum_list = split_sum(s.strip())
    if len(sum_list) == 0:
        return 0
    total = eval_term(sum_list[0])
    for i in range(1, len(sum_list), 2):
        op = sum_list[i]
        item = eval_term(sum_list[i + 1])
        if op == '*':
            total *= item
        else:  # '+'
            total += item
    return total


def eval_sum_part2(s):
    s = s.replace('+', 'A').replace('*', '+').replace('A', '*')
    new_s = ''
    old_t = 0
    for match_group in re.finditer('\\d+', s):
        f, t = match_group.span()
        new_s += s[old_t:f]
        new_s += f'FakeInt({s[f:t]})'
        old_t = t
    new_s += s[old_t:]
    return eval(new_s).value


def part1():
    return sum(eval_sum_part1(l) for l in read_input_as_lines())


def part2():
    return sum(eval_sum_part2(l) for l in read_input_as_lines())


if __name__ == '__main__':
    print(part1())
    print(part2())
