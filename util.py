import time
from functools import reduce


def mult(iterable):
    return reduce(lambda a, b: a * b, iterable)


def time_call(f, *args):
    t1 = time.time()
    result = f(*args)
    print(f'Time taken: {time.time() - t1}')
    return result


def remove_empty(l):
    return filter(None, l)


def safe_split(text, delim):
    return list(remove_empty(text.split(delim)))


def read_input(filename='input'):
    with open(filename) as f:
        return f.read()


def read_input_split(filename, delim):
    return safe_split(read_input(filename=filename), delim)


def read_input_as_lines(filename='input'):
    return read_input_split(filename, '\n')


def read_input_as_numbers(filename='input'):
    return list(map(lambda l: int(l), read_input_as_lines(filename=filename)))


def read_input_as_passports(filename='input'):
    return map(lambda p: p.strip(), read_input_split(filename, '\n\n'))
