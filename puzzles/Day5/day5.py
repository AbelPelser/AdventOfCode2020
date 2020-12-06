from util import read_input_as_lines


def b_search_clever(s, upper_c, lower_c, _):
    return int(s.replace(upper_c, '1').replace(lower_c, '0'), base=2)


def b_search_original(s, lower_c, upper_c, upper_bound_excl):
    lower_bound_incl = 0
    for c in list(s):
        diff = upper_bound_excl - lower_bound_incl
        if c == upper_c:
            lower_bound_incl += diff / 2
        elif c == lower_c:
            upper_bound_excl -= diff / 2
    return int(lower_bound_incl)


def row(s):
    return b_search_clever(s[7:], 'R', 'L', 8)


def col(s):
    return b_search_clever(s[:7], 'B', 'F', 128)


def seat_id(s):
    return row(s) + (col(s) * 8)


def part1():
    return max(seat_id(s) for s in read_input_as_lines())


def part2():
    seat_ids = sorted(list(seat_id(s) for s in read_input_as_lines()))
    for first, second in zip(seat_ids[:-1], seat_ids[1:]):
        if first + 1 != second:
            return first + 1
    raise ValueError('Wut?')


if __name__ == '__main__':
    print(part1())
    print(part2())
