import collections
import re
from pprint import pprint
from typing import Dict, List, Optional, Union

import numpy as np

from util import mult, read_input, safe_split

EMPTY_TILE_ID = -1
TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3

class Border:
    def __init__(self, bit_str: str, owned_by: Optional['Tile']):
        self.value = int(bit_str, 2)
        self.value_inv = int(bit_str[::-1], 2)
        self.owned_by = owned_by
        self.border_link: Optional[Border] = None

    def could_neighbour(self, other: 'Border') -> bool:
        if self == other or self.border_link is not None or other.border_link is not None:
            return False
        res = self.value == other.value or self.value == other.value_inv
        return res

    def link(self, other: 'Border') -> None:
        self.border_link = other
        other.border_link = self

    def __str__(self):
        other_tile_id = 'None' if self.border_link is None else self.border_link.owned_by.tile_id
        return f'{self.value}/{self.value_inv} [{self.owned_by.tile_id} -> {other_tile_id}]'

    def __repr__(self):
        return str(self)


class Tile:
    def __init__(self, tile_id, tile_lines):
        self.tile_id = tile_id
        self.lines = tile_lines
        self.lines_array = np.array([list(map(int, l)) for l in tile_lines])
        self.borders = None

    def trim_edges(self):
        self.lines_array = self.lines_array[1:-1, 1:-1]

    def get_neighbour(self, direction):
        return self.borders[direction].border_link.owned_by

    def rotate_left(self):
        self.borders = self.borders[1:] + [self.borders[0]]
        self.lines_array = np.rot90(self.lines_array)

    def invert_borders(self):
        for border in self.borders:
            value = border.value
            border.value = border.value_inv
            border.value_inv = value

    def mirror(self):
        self.lines_array = np.fliplr(self.lines_array)
        right_border = self.borders[RIGHT]
        self.borders[RIGHT] = self.borders[LEFT]
        self.borders[LEFT] = right_border
        self.invert_borders()

    def __str__(self):
        return f'Tile({self.tile_id}, {self.borders})'

    def __repr__(self):
        return str(self)


def invert_direction(direction):
    return (direction + 2) % 4


def parse_input_as_tiles(text):
    tile_data: Dict[int, Tile] = dict()

    for tile_str in safe_split(text, '\n\n'):
        tile_str = tile_str.replace('#', '1').replace('.', '0')
        tile_id_str, *tile_lines = safe_split(tile_str, '\n')
        tile_id = int(*re.match('Tile ([0-9]+):', tile_id_str).groups())

        tile = Tile(tile_id, tile_lines)
        # top, right, bottom, left
        tile.borders = [Border(tile_lines[0], tile),
                        Border(''.join([l[-1] for l in tile_lines]), tile),
                        Border(tile_lines[-1][::-1], tile),
                        Border(''.join([l[0] for l in tile_lines])[::-1], tile)]
        tile_data[tile_id] = tile
    return tile_data


def find_corner_tiles(tile_data):
    corner_tiles = []
    all_borders = sum([t.borders for t in tile_data.values()], [])
    all_border_values = [b.value for b in all_borders]
    all_border_inv_values = [b.value_inv for b in all_borders]
    for tile in tile_data.values():
        n_unmatched_borders = 0
        for border in tile.borders:
            if border.value not in all_border_inv_values and all_border_values.count(border.value) == 1 and \
                    border.value_inv not in all_border_values and all_border_inv_values.count(border.value_inv) == 1:
                n_unmatched_borders += 1
        if n_unmatched_borders == 2:
            corner_tiles.append(tile)
    return corner_tiles


def match_borders(tile_data):
    empty_space = Tile(EMPTY_TILE_ID, [])
    edge = Border('0', empty_space)
    all_borders = sum([t.borders for t in tile_data.values()], [])
    unmatched_borders = all_borders
    while len(unmatched_borders) > 0:
        for border in unmatched_borders:
            potential_matches = [b for b in unmatched_borders if border.could_neighbour(b)]
            if len(potential_matches) == 0:
                border.link(edge)
                break
            elif len(potential_matches) == 1:
                border.link(potential_matches[0])
                break
        unmatched_borders = [b for b in unmatched_borders if not b.border_link]


def find_and_rotate_next_tile(current_tile, direction):
    current_border = current_tile.borders[direction]
    next_border = current_border.border_link
    next_tile = next_border.owned_by
    if current_border.value != next_border.value_inv:
        next_tile.mirror()
    while next_tile.borders.index(next_border) != invert_direction(direction):
        next_tile.rotate_left()
    return next_tile


def assemble_img(tile_data):
    for tile in tile_data.values():
        tile.trim_edges()
    start_corner = find_corner_tiles(tile_data)[0]

    while start_corner.get_neighbour(RIGHT).tile_id == EMPTY_TILE_ID or \
            start_corner.get_neighbour(BOTTOM).tile_id == EMPTY_TILE_ID:
        start_corner.rotate_left()

    current_tile = start_corner
    grid_size = int(len(tile_data.values()) ** 0.5)
    row_lists = [[] for _ in range(grid_size)]
    row_lists[0].append(current_tile.lines_array)

    for tile_i in range(1, grid_size**2):
        row_i = tile_i // grid_size
        if tile_i % grid_size == 0:
            direction = BOTTOM
        else:
            direction = RIGHT if row_i % 2 == 0 else LEFT
        next_tile = find_and_rotate_next_tile(current_tile, direction)
        row_lists[row_i].append(next_tile.lines_array)
        current_tile = next_tile

    row_arrays = []
    for i in range(len(row_lists)):
        # Reverse every 2nd row, since we snaked our way through the puzzle
        row_list = row_lists[i] if i % 2 == 0 else list(reversed(row_lists[i]))
        row_arrays.append(np.concatenate(row_list, axis=1))
    return np.concatenate(row_arrays)


def part1():
    return mult(t.tile_id for t in find_corner_tiles(parse_input_as_tiles(read_input())))


def find_seamonsters_in_img(img):
    img2 = np.where(img == 1, '#', img)
    img2 = np.where(img == 0, '.', img2)

    sea_monster_str = "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   "
    sea_monster_arr = np.array(list(map(list, sea_monster_str.split('\n'))))
    sea_monster_match_arr = sea_monster_arr == '#'
    sea_monster_width = len(sea_monster_arr[0])
    sea_monster_height = len(sea_monster_arr)
    n_seamonsters = 0
    for i in range(len(img2) - sea_monster_width):
        for j in range(len(img2[0]) - sea_monster_height):
            img_part = img2[j:j+sea_monster_height, i:i+sea_monster_width]
            img_part_matches = img_part == sea_monster_arr
            if np.all(img_part_matches == sea_monster_match_arr):
                n_seamonsters += 1
                img_part[img_part_matches] = 'O'
    return np.sum(img2 == '#'), n_seamonsters


def part2():
    text = read_input()

    tile_data = parse_input_as_tiles(text)
    match_borders(tile_data)
    img = assemble_img(tile_data)
    n_seamonsters = 0
    roughness = None
    for _ in range(4):
        roughness, n_seamonsters = find_seamonsters_in_img(img)
        if n_seamonsters > 0:
            break
        img = np.rot90(img)
    if n_seamonsters == 0:
        img = np.flipud(img)
        for _ in range(4):
            roughness, n_seamonsters = find_seamonsters_in_img(img)
            if n_seamonsters > 0:
                break
            img = np.rot90(img)
    assert roughness is not None
    return roughness


if __name__ == '__main__':
    print(part1())
    print(part2())
