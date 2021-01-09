import re

import numpy as np

from util import mult, read_input, safe_split

# import cv2

EMPTY_TILE_ID = -1
DIRECTIONS = list(range(4))
TOP, RIGHT, BOTTOM, LEFT = DIRECTIONS


class Border:
    def __init__(self, value_str, owned_by):
        self.value = value_str
        self.value_inv = value_str[::-1]
        self.owned_by = owned_by
        self.border_link = None

    def could_neighbour(self, other):
        if self == other or self.border_link is not None or other.border_link is not None:
            return False
        return self.value == other.value or self.value == other.value_inv

    def link(self, other):
        self.border_link = other
        other.border_link = self


class Tile:
    def __init__(self, tile_id, tile_lines):
        self.tile_id = tile_id
        self.lines = tile_lines
        self.lines_array = np.array(list(map(list, tile_lines)))
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

    def is_edge(self, direction):
        return self.get_neighbour(direction).tile_id == EMPTY_TILE_ID

    def is_corner(self):
        return len([d for d in DIRECTIONS if self.is_edge(d)]) == 2


def invert_direction(direction):
    return (direction + 2) % 4


def parse_input_as_tiles(text):
    tile_data = dict()

    for tile_str in safe_split(text, '\n\n'):
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
    return list(filter(lambda t: t.is_corner(), tile_data.values()))


def match_borders(tile_data):
    empty_space = Tile(EMPTY_TILE_ID, [])
    edge = Border('0', empty_space)
    all_borders = sum([t.borders for t in tile_data.values()], [])
    unmatched_borders = all_borders
    while len(unmatched_borders) > 0:
        for border in unmatched_borders:
            if border.border_link:
                # If matched during previous iteration, ignore
                continue
            potential_matches = [b for b in unmatched_borders if border.could_neighbour(b)]
            if len(potential_matches) == 0:
                border.link(edge)
            elif len(potential_matches) == 1:
                border.link(potential_matches[0])
        unmatched_borders = [b for b in unmatched_borders if not b.border_link]


def find_and_rotate_next_tile(current_tile, border_direction):
    border = current_tile.borders[border_direction]
    neighbour_border = border.border_link
    next_tile = neighbour_border.owned_by
    if border.value != neighbour_border.value_inv:
        next_tile.mirror()
    target_direction = invert_direction(border_direction)
    while next_tile.borders.index(neighbour_border) != target_direction:
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

    for tile_i in range(1, grid_size ** 2):
        row_i = tile_i // grid_size
        if tile_i % grid_size == 0:
            # End of line, go down
            direction = BOTTOM
        else:
            # Alternate between left and right
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


def find_sea_monsters_in_img(img):
    sea_monster_str = "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   "
    sea_monster_arr = np.array(list(map(list, sea_monster_str.split('\n'))))
    sea_monster_match_arr = sea_monster_arr == '#'
    sea_monster_width = len(sea_monster_arr[0])
    sea_monster_height = len(sea_monster_arr)

    # res = cv2.matchTemplate(img, sea_monster_arr, cv2.TM_CCOEFF_NORMED)

    n_sea_monsters = 0
    for i in range(len(img) - sea_monster_width):
        for j in range(len(img[0]) - sea_monster_height):
            img_part = img[j:j + sea_monster_height, i:i + sea_monster_width]
            img_part_matches = img_part == sea_monster_arr
            if np.all(img_part_matches == sea_monster_match_arr):
                n_sea_monsters += 1
                img_part[img_part_matches] = 'O'
    return np.sum(img == '#'), n_sea_monsters


def part1():
    tile_data = parse_input_as_tiles(read_input())
    match_borders(tile_data)
    return mult(t.tile_id for t in find_corner_tiles(tile_data))


def part2():
    tile_data = parse_input_as_tiles(read_input())
    match_borders(tile_data)
    img = assemble_img(tile_data)

    def find_roughness(image):
        for _ in range(4):
            roughness, n_sea_monsters = find_sea_monsters_in_img(image)
            if n_sea_monsters > 0:
                return roughness
            image = np.rot90(image)

    return find_roughness(img) or find_roughness(np.flipud(img))


if __name__ == '__main__':
    print(part1())
    print(part2())
