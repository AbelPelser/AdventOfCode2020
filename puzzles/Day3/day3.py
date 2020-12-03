from util import read_input_as_lines


def parse_lines(lines):
    for line in lines:
        policy, letter, password = line.split(' ')
        int_a_str, int_b_str = policy.split('-')
        letter = letter[:-1]
        yield int(int_a_str), int(int_b_str), letter, password


def count_valid(lines, validator):
    return sum(int(validator(low, high, letter, password))
               for low, high, letter, password in parse_lines(lines))


def part1_validator(low, high, letter, password):
    return low <= password.count(letter) <= high


def part2_validator(low, high, letter, password):
    # No index 0
    return (password[low - 1] == letter) ^ (password[high - 1] == letter)


def part1():
    return count_valid(read_input_as_lines(), part1_validator)


def part2():
    return count_valid(read_input_as_lines(), part2_validator)


if __name__ == '__main__':
    print(part1())
    print(part2())
