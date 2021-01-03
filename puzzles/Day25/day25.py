from util import read_input_as_lines


def transform(subject, loop_size):
    return pow(subject, loop_size, 20201227)


def part1():
    pub_key_a, pub_key_b = list(map(int, read_input_as_lines()))

    n = 0
    while True:
        x = transform(7, n)
        if x == pub_key_a:
            return transform(pub_key_b, n)
        if x == pub_key_b:
            return transform(pub_key_a, n)
        n += 1


def part2():
    return 'Looks like you only needed 49 stars after all.'


if __name__ == '__main__':
    print(part1())
    print(part2())
