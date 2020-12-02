import time
from functools import reduce


def mult(iterable):
    return reduce(lambda a, b: a * b, iterable)


def time_call(f, *args):
    t1 = time.time()
    f(*args)
    print(f'Time taken: {time.time() - t1}')


def read_input_as_lines(filename='input'):
    with open(filename) as f:
        return filter(None, f.read().split('\n'))


def read_input_as_numbers(filename='input'):
    return map(lambda l: int(l), read_input_as_lines(filename=filename))
