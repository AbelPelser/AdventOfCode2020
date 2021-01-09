import re
from collections import defaultdict

from util import read_input_as_lines

direction_steps = {
    'e': (2, 0),
    'se': (1, -2),
    'sw': (-1, -2),
    'nw': (-1, 2),
    'w': (-2, 0),
    'ne': (1, 2)
}


def get_neighbour_coords(e, n):
    return [(e + d_e, n + d_n) for d_e, d_n in direction_steps.values()]


def parse_line(line):
    e = n = 0
    while line:
        direction, line = re.match('([ns]?[ew])([nsew]*)', line).groups()
        d_e, d_n = direction_steps[direction]
        e += d_e
        n += d_n
    return e, n


def parse_input(lines):
    tiles = defaultdict(bool)
    # False is white, True is black
    for line in lines:
        e, n = parse_line(line)
        tiles[(e, n)] = not tiles[(e, n)]
    return tiles


def enliven_art(tiles, rounds):
    for _ in range(rounds):
        coords_to_process = set(tiles.keys())
        coords_to_process.update(*(get_neighbour_coords(e, n) for e, n in tiles.keys()))
        new_tiles = defaultdict(bool)
        for e, n in coords_to_process:
            n_black_neighbours = sum(tiles[(e_, n_)] for e_, n_ in get_neighbour_coords(e, n))
            if (tiles[(e, n)] and 1 <= n_black_neighbours <= 2) or n_black_neighbours == 2:
                new_tiles[(e, n)] = True
        tiles = new_tiles
    return tiles


def part1():
    return sum(parse_input(read_input_as_lines()).values())


def part2():
    return sum(enliven_art(parse_input(read_input_as_lines()), 100).values())


if __name__ == '__main__':
    print(part1())
    print(part2())
