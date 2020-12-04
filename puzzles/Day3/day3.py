from util import mult, read_input_as_lines


def part1():
    return find_n_tree_in_path(read_input_as_lines(), 3, 1)


def part2():
    return mult(find_n_tree_in_path(read_input_as_lines(), x_d, y_d)
                for x_d, y_d in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)))


def find_n_tree_in_path(map_data, x_d, y_d):
    x = 0
    total = 0
    for y in range(0, len(map_data), y_d):
        line = map_data[y]
        if line[x % len(line)] == '#':
            total += 1
        x += x_d
    return total


if __name__ == '__main__':
    print(part1())  # 176
    print(part2())  # 5872458240
