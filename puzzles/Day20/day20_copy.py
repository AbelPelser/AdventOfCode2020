import collections
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
    def __init__(self, tile_id: int, tile_lines: List[str]):
        self.tile_id = tile_id
        self.lines: List[str] = tile_lines
        self.lines_array = np.array([[int(c) for c in list(l)] for l in tile_lines])

        self.borders: Optional[List[Border]] = None

        self.tile_top: Optional[Tile]
        self.tile_right: Optional[Tile]
        self.tile_bottom: Optional[Tile]
        self.tile_left: Optional[Tile]

        self.rotation_degrees: int = 0
        self.mirrored: bool = False

    def trim_edges(self):
        self.lines_array = self.lines_array[1:-1, 1:-1]

    def rotate_left(self):
        self.rotation_degrees = (self.rotation_degrees - 90) % 360
        self.borders = self.borders[1:] + [self.borders[0]]
        self.lines_array = np.rot90(self.lines_array)

    def rotate_right(self):
        self.rotation_degrees = (self.rotation_degrees + 90) % 360
        self.borders = [self.borders[-1]] + self.borders[:-1]
        for _ in range(3):
            self.lines_array = np.rot90(self.lines_array)

    def flip_borders(self):
        for b in self.borders:
            value = b.value
            b.value = b.value_inv
            b.value_inv = value

    def flip_vertically(self):
        self.lines_array = np.flipud(self.lines_array)
        bottom_border = self.borders[BOTTOM]
        self.borders[BOTTOM] = self.borders[TOP]
        self.borders[TOP] = bottom_border
        self.flip_borders()

    def flip_horizontally(self):
        self.lines_array = np.fliplr(self.lines_array)
        right_border = self.borders[RIGHT]
        self.borders[RIGHT] = self.borders[LEFT]
        self.borders[LEFT] = right_border
        self.flip_borders()

    def __str__(self):
        return f'Tile({self.tile_id}, {self.borders})'

    def __repr__(self):
        return str(self)


def parse_input_as_tiles(text: str) -> Dict[int, Tile]:
    tiles_str = safe_split(text, '\n\n')
    tile_data: Dict[int, Tile] = dict()

    for tile_str in tiles_str:
        tile_str: str = tile_str.replace('#', '1').replace('.', '0')
        tile_lines: List[str] = safe_split(tile_str, '\n')
        tile_id: int = int(tile_lines[0].split('Tile ')[-1].split(':')[0])
        tile_lines = tile_lines[1:]

        border_top_str = tile_lines[0]
        border_right_str = ''.join([l[-1] for l in tile_lines])
        border_bottom_str = tile_lines[-1][::-1]
        border_left_str = ''.join([l[0] for l in tile_lines])[::-1]

        tile = Tile(tile_id, tile_lines)
        borders = [Border(border_top_str, tile),
                   Border(border_right_str, tile),
                   Border(border_bottom_str, tile),
                   Border(border_left_str, tile)]
        tile.borders = borders
        tile_data[tile_id] = tile
    return tile_data


def find_corner_tiles(tile_data: Dict[int, Tile]) -> List[Tile]:
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


def match_borders(tile_data: Dict[int, Tile]):
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


def assemble_img(tile_data: Dict[int, Tile]) -> np.array:
    for tile in tile_data.values():
        tile.trim_edges()
    start_corner = find_corner_tiles(tile_data)[0]

    while start_corner.borders[RIGHT].border_link.owned_by.tile_id == EMPTY_TILE_ID or \
            start_corner.borders[BOTTOM].border_link.owned_by.tile_id == EMPTY_TILE_ID:
        start_corner.rotate_right()

    row_i = 0
    current_tile = row_start = start_corner
    row_arrays = [[] for _ in range(GRID_SIZE)]
    row_arrays[row_i].append(current_tile.lines_array)


    for row_i in range(GRID_SIZE):
        # if row_i == 0:
        #     pass
        # else:
        #     row_start = row_arrays
        for _ in range(GRID_SIZE - 1):
            direction = RIGHT if (row_i % 2) == 0 else LEFT
            current_border = current_tile.borders[direction]
            next_border = current_border.border_link
            next_tile = next_border.owned_by



    while True:
        if current_tile.borders[RIGHT].border_link.owned_by.tile_id != EMPTY_TILE_ID:
            direction = RIGHT
            current_border = current_tile.borders[direction]
            next_border = current_border.border_link
            next_tile = next_border.owned_by
        elif current_tile.borders[BOTTOM].border_link.owned_by.tile_id != EMPTY_TILE_ID:
            direction = BOTTOM
            current_border = row_start.borders[direction]
            next_border = current_border.border_link
            next_tile = next_border.owned_by
            row_start = next_tile
            row_i += 1
        else:
            break
        if current_border.value != next_border.value_inv:
            next_tile.flip_horizontally()
        while next_tile.borders.index(next_border) != ((direction + 2) % 4):
            next_tile.rotate_right()
        row_arrays[row_i].append(next_tile.lines_array)
        current_tile = next_tile

    for i in range(len(row_arrays)):
        row_arrays[i] = np.concatenate(row_arrays[i], axis=1)
    return np.concatenate(row_arrays)


def part1_hacky(tile_data: Dict[int, Tile]) -> int:
    return mult(t.tile_id for t in find_corner_tiles(tile_data))


def part2_hackier(img):
    img1 = np.where(img == 1, '#', img)
    img2 = np.where(img == 0, '.', img1)

    sea_monster_str = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
    sea_monster_arr = np.array([list(l) for l in sea_monster_str.split('\n')])
    sea_monster_match_arr = sea_monster_arr == '#'
    sea_monster_width = len(sea_monster_arr[0])
    sea_monster_height = len(sea_monster_arr)
    n_seamonsters = 0
    for i in range(len(img1) - sea_monster_width):
        for j in range(len(img2[0]) - sea_monster_height):
            img_part = img2[j:j+sea_monster_height, i:i+sea_monster_width]
            img_part_matches = img_part == sea_monster_arr
            if np.all(img_part_matches == sea_monster_match_arr):
                n_seamonsters += 1
                img_part[img_part_matches] = 'O'
    return np.sum(img2 == '#'), n_seamonsters


if __name__ == '__main__':
    text = read_input()

    tile_data = parse_input_as_tiles(text)

    GRID_SIZE = int(len(tile_data.values()) ** 0.5)

    match_borders(tile_data)

    img = assemble_img(tile_data)
    n_seamonsters = 0
    for _ in range(4):
        answer, n_seamonsters = part2_hackier(img)
        if n_seamonsters > 0:
            break
        img = np.rot90(img)
    if n_seamonsters == 0:
        img = np.flipud(img)
        for _ in range(4):
            answer, n_seamonsters = part2_hackier(img)
            if n_seamonsters > 0:
                break
            img = np.rot90(img)

    print(part1_hacky(tile_data))
    print(answer)
