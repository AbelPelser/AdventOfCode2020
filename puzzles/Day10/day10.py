from util import mult, read_input_as_numbers


def read_all_voltages_sorted(filename='input'):
    numbers = sorted(read_input_as_numbers(filename=filename))
    if numbers[0] != 0:
        numbers = [0] + numbers
    numbers.append(max(numbers) + 3)
    return numbers


def get_n_combinations(number_sorted, i=0):
    if i == len(number_sorted) - 1:
        return 1
    count = 0
    j = i + 1
    while j < len(number_sorted) and (number_sorted[j] - number_sorted[i]) <= 3:
        count += get_n_combinations(number_sorted, j)
        j += 1
    return count


def partition_input(numbers):
    partition_start = 0
    partitions = []
    for i in range(1, len(numbers)):
        if numbers[i] - numbers[i - 1] == 3:
            partitions.append(numbers[partition_start:i])
            partition_start = i
    partitions.append(numbers[partition_start:len(numbers)])
    return partitions


def part1():
    voltages = read_all_voltages_sorted()
    # Differences of 2 don't occur
    differences = {1: 0, 3: 0}
    for i in range(1, len(voltages)):
        differences[voltages[i] - voltages[i - 1]] += 1
    return differences[1] * differences[3]


def part2():
    return mult(get_n_combinations(partition) for partition in partition_input(read_all_voltages_sorted()))


if __name__ == '__main__':
    print(part1())
    print(part2())
