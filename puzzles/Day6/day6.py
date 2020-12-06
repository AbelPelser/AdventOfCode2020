from util import read_input, safe_split


def text_to_groups(text):
    yield from safe_split(text, '\n\n')


def group_to_persons(group_text):
    yield from safe_split(group_text, '\n')


def group_to_unique_answers(group_text):
    return (set(person) for person in group_to_persons(group_text))


def helper(text, group_parser):
    return sum(len(group_parser(*group_to_unique_answers(group))) for group in text_to_groups(text))


def part1():
    return helper(read_input(), set.union)


def part2():
    return helper(read_input(), set.intersection)


if __name__ == '__main__':
    print(part1())
    print(part2())
