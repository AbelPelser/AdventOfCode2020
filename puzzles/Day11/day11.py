import copy
from collections import defaultdict

from util import read_input_as_lines

EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'
FLOOR = '.'


def get_seat_in_line_of_sight(lines, row, col, d_row, d_col, max_sight=None):
    row += d_row
    col += d_col
    sight_length = 1
    while 0 <= row < len(lines) and 0 <= col < len(lines[row]) and (not max_sight or sight_length <= max_sight):
        if lines[row][col] != FLOOR:
            return row, col
        row += d_row
        col += d_col
        sight_length += 1
    return None


def get_neighbour_direction_steps():
    return (-1, -1), (-1, 0), (-1, 1), (1, 0), (1, -1), (1, 1), (0, -1), (0, 1)


def find_seats_in_sight(lines, max_sight=None):
    seats_in_sight = defaultdict(set)
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            for d_row, d_col in get_neighbour_direction_steps():
                seat_in_sight = get_seat_in_line_of_sight(lines, row, col, d_row, d_col, max_sight=max_sight)
                if seat_in_sight:
                    seats_in_sight[row, col].add(seat_in_sight)
    return seats_in_sight


def get_n_occupied_neighbors(lines, seats_in_sight, row, col):
    return sum(lines[r_s][c_s] == OCCUPIED_SEAT for r_s, c_s in seats_in_sight[row, col])


def step(lines, seats_in_sight, max_acceptable_neighbors):
    new_lines = copy.deepcopy(lines)
    change = False
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            n_occupied = get_n_occupied_neighbors(lines, seats_in_sight, row, col)
            if n_occupied == 0 and lines[row][col] == EMPTY_SEAT:
                new_lines[row][col] = OCCUPIED_SEAT
                change = True
            elif n_occupied >= max_acceptable_neighbors and lines[row][col] == OCCUPIED_SEAT:
                new_lines[row][col] = EMPTY_SEAT
                change = True
    return new_lines, change


def find_balance_occupied(max_acceptable_neighbors, max_sight=None):
    lines = [list(line) for line in read_input_as_lines()]
    seats_in_sight = find_seats_in_sight(lines, max_sight=max_sight)
    while True:
        new_lines, change = step(lines, seats_in_sight, max_acceptable_neighbors)
        if not change:
            return sum(lines, []).count(OCCUPIED_SEAT)
        lines = new_lines


def part1():
    return find_balance_occupied(4, 1)


def part2():
    return find_balance_occupied(5)


if __name__ == '__main__':
    print(part1())
    print(part2())
