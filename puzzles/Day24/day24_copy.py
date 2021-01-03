from collections import defaultdict

from util import read_input_as_lines


def get_neighbour_coords(e, n):
    return [(e + 1, n),
            (e + 0.5, n - 1),
            (e - 0.5, n - 1),
            (e - 0.5, n + 1),
            (e - 1, n),
            (e + 0.5, n + 1)]


if __name__ == '__main__':
    lines = read_input_as_lines()
    #     lines = """sesenwnenenewseeswwswswwnenewsewsw
    # neeenesenwnwwswnenewnwwsewnenwseswesw
    # seswneswswsenwwnwse
    # nwnwneseeswswnenewneswwnewseswneseene
    # swweswneswnenwsewnwneneseenw
    # eesenwseswswnenwswnwnwsewwnwsene
    # sewnenenenesenwsewnenwwwse
    # wenwwweseeeweswwwnwwe
    # wsweesenenewnwwnwsenewsenwwsesesenwne
    # neeswseenwwswnwswswnw
    # nenwswwsewswnenenewsenwsenwnesesenew
    # enewnwewneswsewnwswenweswnenwsenwsw
    # sweneswneswneneenwnewenewwneswswnese
    # swwesenesewenwneswnwwneseswwne
    # enesenwswwswneneswsenwnewswseenwsese
    # wnwnesenesenenwwnenwsewesewsesesew
    # nenewswnwewswnenesenwnesewesw
    # eneswnwswnwsenenwnwnwwseeswneewsenese
    # neswnwewnwnwseenwseesewsenwsweewe
    # wseweeenwnesenwwwswnew""".split('\n')
    #  / \
    # |   |
    #  \ /
    #
    tiles = defaultdict(bool)
    # False is white, True is black
    for line in lines:
        e = n = 0
        while len(line) > 0:
            if line.startswith('e'):
                e += 1
                line = line[1:]
            elif line.startswith('se'):
                e += 0.5
                n -= 1
                line = line[2:]
            elif line.startswith('sw'):
                e -= 0.5
                n -= 1
                line = line[2:]
            elif line.startswith('nw'):
                e -= 0.5
                n += 1
                line = line[2:]
            elif line.startswith('w'):
                e -= 1
                line = line[1:]
            elif line.startswith('ne'):
                e += 0.5
                n += 1
                line = line[2:]
        e = int(round(10 * e))
        # print(e, n)
        tiles[(e, n)] = not tiles[(e, n)]
    print(sum(tiles.values()))
