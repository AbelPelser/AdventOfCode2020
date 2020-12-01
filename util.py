from functools import reduce


def mult(iterable):
    return reduce(lambda a, b: a * b, iterable)


def read_input(filename='input'):
    with open(filename) as f:
        return list(map(lambda l: int(l), filter(None, f.read().split('\n'))))
