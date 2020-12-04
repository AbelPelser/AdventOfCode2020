import time
from functools import reduce


def mult(iterable):
    return reduce(lambda a, b: a * b, iterable)


def time_call(f, *args):
    t1 = time.time()
    f(*args)
    print(f'Time taken: {time.time() - t1}')


def read_input_split(filename, delim):
    with open(filename) as f:
        return list(filter(None, f.read().split(delim)))


def read_input_as_lines(filename='input'):
    return read_input_split(filename, '\n')


def read_input_as_numbers(filename='input'):
    return list(map(lambda l: int(l), read_input_as_lines(filename=filename)))


def read_input_as_passports(filename='input'):
    return map(lambda p: p.strip(), read_input_split(filename, '\n\n'))
