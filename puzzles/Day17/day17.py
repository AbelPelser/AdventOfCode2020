import copy
import itertools

from util import read_input_as_lines

# from scipy import sp

ACTIVE = '#'
INACTIVE = '.'

GRID_SIZE = 26
OFFSET = int(GRID_SIZE / 2) - 4


# fake to real
def get_c1(x, y, z):
    return x + OFFSET, y + OFFSET, z + OFFSET


# fake to real
def get_c2(x, y, z, a):
    return x + OFFSET, y + OFFSET, z + OFFSET, a + OFFSET


# real
def get_all_real_coords(n_dimensions):
    return list(itertools.product(range(GRID_SIZE), repeat=n_dimensions))


def parse_grid1(lines):
    grid = []
    for _ in range(GRID_SIZE):
        grid.append([])
        for _ in range(GRID_SIZE):
            grid[-1].append([])
            for _ in range(GRID_SIZE):
                grid[-1][-1].append(INACTIVE)
    for y, line in enumerate(lines):
        for x, c in enumerate(list(line)):
            assert c in [ACTIVE, INACTIVE], c
            new_x, new_y, new_z = get_c1(x, y, 0)
            grid[new_x][new_y][new_z] = c
    return grid


def parse_grid2(lines):
    grid = []
    for _ in range(GRID_SIZE):
        grid.append([])
        for _ in range(GRID_SIZE):
            grid[-1].append([])
            for _ in range(GRID_SIZE):
                grid[-1][-1].append([])
                for _ in range(GRID_SIZE):
                    grid[-1][-1][-1].append(INACTIVE)
    for y, line in enumerate(lines):
        for x, c in enumerate(list(line)):
            assert c in [ACTIVE, INACTIVE], c
            new_x, new_y, new_z, new_a = get_c2(x, y, 0, 0)
            grid[new_x][new_y][new_z][new_a] = c
    return grid


def get_neighbors_steps(n_dimensions):
    result = list(itertools.product([-1, 0, 1], repeat=n_dimensions))
    result.remove(tuple((0 for _ in range(n_dimensions))))
    return result


def is_in_grid(val):
    return 0 <= val < GRID_SIZE


# real to real
def get_neighbour_coords1(x, y, z):
    result = []
    for d_x, d_y, d_z in get_neighbors_steps(n_dimensions=3):
        new_x, new_y, new_z = x + d_x, y + d_y, z + d_z
        if not (is_in_grid(new_x) and is_in_grid(new_y) and is_in_grid(new_z)):
            continue
        result.append((new_x, new_y, new_z))
    return result


def get_neighbour_coords2(x, y, z, a):
    result = []
    for d_x, d_y, d_z, d_a in get_neighbors_steps(4):
        new_x, new_y, new_z, new_a = x + d_x, y + d_y, z + d_z, a + d_a
        if not (is_in_grid(new_x) and is_in_grid(new_y) and is_in_grid(new_z) and is_in_grid(new_a)):
            continue
        result.append((new_x, new_y, new_z, new_a))
    return result


# real
def get_neighbours1(grid, x, y, z):
    return [grid[nb_x][nb_y][nb_z] for nb_x, nb_y, nb_z in get_neighbour_coords1(x, y, z)]


def get_neighbours2(grid, x, y, z, a):
    return [grid[nb_x][nb_y][nb_z][nb_a] for nb_x, nb_y, nb_z, nb_a in get_neighbour_coords2(x, y, z, a)]


# real
def get_n_active_neighbours1(grid, x, y, z):
    return len(list(filter(lambda c: c == ACTIVE, get_neighbours1(grid, x, y, z))))


def get_n_active_neighbours2(grid, x, y, z, a):
    return len(list(filter(lambda c: c == ACTIVE, get_neighbours2(grid, x, y, z, a))))


def step_part1(grid):
    new_grid = copy.deepcopy(grid)
    for x, y, z in get_all_real_coords(3):
        val = grid[x][y][z]
        n_active_neighbours = get_n_active_neighbours1(grid, x, y, z)
        if val == ACTIVE and n_active_neighbours not in [2, 3]:
            new_grid[x][y][z] = INACTIVE
        elif val == INACTIVE and n_active_neighbours == 3:
            new_grid[x][y][z] = ACTIVE
        else:
            new_grid[x][y][z] = grid[x][y][z]
    return new_grid


def step_part2(grid):
    new_grid = copy.deepcopy(grid)
    for x, y, z, a in get_all_real_coords(4):
        val = grid[x][y][z][a]
        n_active_neighbours = get_n_active_neighbours2(grid, x, y, z, a)
        if val == ACTIVE and n_active_neighbours not in [2, 3]:
            new_grid[x][y][z][a] = INACTIVE
        elif val == INACTIVE and n_active_neighbours == 3:
            new_grid[x][y][z][a] = ACTIVE
        else:
            new_grid[x][y][z][a] = grid[x][y][z][a]
    return new_grid


def get_n_active_cubes1(grid):
    count = 0
    for x, y, z in get_all_real_coords(3):
        count += int(grid[x][y][z] == ACTIVE)
    return count


def get_n_active_cubes2(grid):
    count = 0
    for x, y, z, a in get_all_real_coords(4):
        count += int(grid[x][y][z][a] == ACTIVE)
    return count


def print_grid1(grid):
    output = ''
    for z in range(GRID_SIZE):
        output_layer = f'z={z - OFFSET}\n'
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                output_layer += grid[x][y][z]
            output_layer += '\n'
        output_layer += '\n'
        if ACTIVE in output_layer:
            output += output_layer
    print(output)


def print_grid2(grid):
    output = ''
    for z in range(GRID_SIZE):
        for a in range(GRID_SIZE):
            output_layer = f'z={z - OFFSET}, a={a - OFFSET}\n'
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    output_layer += grid[x][y][z][a]
                output_layer += '\n'
            output_layer += '\n'
            if ACTIVE in output_layer:
                output += output_layer
    print(output)


def part1():
    grid = parse_grid1(read_input_as_lines())
    for _ in range(6):
        grid = step_part1(grid)
    return get_n_active_cubes1(grid)  # 315


def part2():
    grid = parse_grid2(read_input_as_lines())
    for _ in range(6):
        grid = step_part2(grid)
    return get_n_active_cubes2(grid)


if __name__ == '__main__':
    print(part1())
    print(part2())