import time

import z3

from util import mult, read_input


def find_sum_combo_with_z3(numbers, n, target=2020):
    solver = z3.Solver()

    symvars = [z3.Int(f'sv_{i}') for i in range(n)]
    solver.add(z3.Sum(symvars) == target)
    solver.add(z3.Distinct(symvars))

    for sv in symvars:
        solver.add(z3.Or([sv == number for number in numbers]))

    if str(solver.check()) == 'sat':
        print(f'Model = {solver.model()}')
        return mult(solver.model()[sv].as_long() for sv in symvars)
    else:
        print('No solution')
        return -1


def part1(numbers):
    return find_sum_combo_with_z3(numbers, 2)


def part2(numbers):
    return find_sum_combo_with_z3(numbers, 3)


if __name__ == '__main__':
    input_numbers = read_input()
    t1 = time.time()
    print(part1(input_numbers))
    print(part2(input_numbers))
    print(f'Time taken: {time.time() - t1}')
