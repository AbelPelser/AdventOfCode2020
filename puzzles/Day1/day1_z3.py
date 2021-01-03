import z3

from util import mult, read_input_as_numbers


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


def part1_z3():
    return find_sum_combo_with_z3(read_input_as_numbers(), 2)


def part2_z3():
    return find_sum_combo_with_z3(read_input_as_numbers(), 3)


if __name__ == '__main__':
    print(part1_z3())
    print(part2_z3())
