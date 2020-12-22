import copy
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

from util import read_input_as_lines, time_call

EMPTY_SEAT_N = 0
OCCUPIED_SEAT_N = 1
FLOOR_N = 2
SEAT_CHAR_MAP: Dict[str, int] = {'L': EMPTY_SEAT_N, '#': OCCUPIED_SEAT_N, '.': FLOOR_N}


def get_seat_in_line_of_sight(lines: [List[List[int]]], row, col, d_row, d_col, max_sight=None) -> \
        Optional[Tuple[int, int]]:
    row += d_row
    col += d_col
    sight_length = 1
    while 0 <= row < len(lines) and 0 <= col < len(lines[row]) and \
            (not max_sight or sight_length <= max_sight):
        if lines[row][col] == FLOOR_N:
            row += d_row
            col += d_col
            sight_length += 1
        else:
            return row, col
    return None


def find_seats_in_sight(lines: List[List[int]], max_sight=None) -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
    seats_in_sight = defaultdict(set)
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            for d_row, d_col in (-1, -1), (-1, 0), (-1, 1), (1, 0), (1, -1), (1, 1), (0, -1), (0, 1):
                seat_in_sight = get_seat_in_line_of_sight(lines, row, col, d_row, d_col, max_sight=max_sight)
                if seat_in_sight:
                    seats_in_sight[row, col].add(seat_in_sight)
    return seats_in_sight


def get_n_occupied_neighbors(lines: List[List[int]], seats_in_sight: Dict[Tuple[int, int], Set[Tuple[int, int]]], row,
                             col) -> int:
    return sum(lines[r_s][c_s] == OCCUPIED_SEAT_N for r_s, c_s in seats_in_sight[row, col])


def step(lines: List[List[int]], seats_in_sight: Dict[Tuple[int, int], Set[Tuple[int, int]]],
         max_acceptable_neighbors) -> Tuple[List[List[int]], bool]:
    new_lines = copy.deepcopy(lines)
    change = False
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            n_occupied = get_n_occupied_neighbors(lines, seats_in_sight, row, col)
            if n_occupied == 0 and lines[row][col] == EMPTY_SEAT_N:
                new_lines[row][col] = OCCUPIED_SEAT_N
                change = True
            elif n_occupied >= max_acceptable_neighbors and lines[row][col] == OCCUPIED_SEAT_N:
                new_lines[row][col] = EMPTY_SEAT_N
                change = True
    return new_lines, change


def find_balance_occupied(max_acceptable_neighbors: int, max_sight=None) -> int:
    lines = [list(map(lambda c: SEAT_CHAR_MAP[c], list(line))) for line in read_input_as_lines()]
    seats_in_sight = find_seats_in_sight(lines, max_sight=max_sight)
    while True:
        new_lines, change = step(lines, seats_in_sight, max_acceptable_neighbors)
        if not change:
            return sum(lines, []).count(OCCUPIED_SEAT_N)
        lines = new_lines


def part1():
    return find_balance_occupied(4, 1)


def part2():
    return find_balance_occupied(5)


if __name__ == '__main__':
    print(time_call(part1))
    print(time_call(part2))
