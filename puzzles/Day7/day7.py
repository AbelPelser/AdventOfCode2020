import re
from collections import defaultdict

from util import read_input_as_lines, remove_empty

SHINY_GOLD = 'shiny gold'


def get_all_containers(bag_dict, bag_type):
    return set.union({bag_type}, *[get_all_containers(bag_dict, bag_type_container)
                                   for bag_type_container in bag_dict[bag_type]])


def get_n_bags_contained(bag_dict, bag_type):
    return sum(amount * (1 + get_n_bags_contained(bag_dict, bag_type_contained))
               for amount, bag_type_contained in bag_dict[bag_type])


def parse_line(line):
    bag_type, bags_contained_str = re.fullmatch('([a-z ]+) bags contain ([a-z0-9, ]*).', line).groups()
    bags_contained_list = []
    for bag in bags_contained_str.split(', '):
        amount, bag_type_contained = remove_empty(
            re.fullmatch('(?:(no) (other bags))|(?:([0-9]+) ([a-z ]+) bags?)', bag).groups())
        if amount != 'no':
            bags_contained_list.append((int(amount), bag_type_contained))
    return bag_type, bags_contained_list


def parse_container_to_contained():
    bag_dict = defaultdict(list)
    for line in read_input_as_lines():
        bag_type, bags_contained_list = parse_line(line)
        bag_dict[bag_type] += bags_contained_list
    return bag_dict


def parse_contained_to_container():
    bag_dict = defaultdict(list)
    for line in read_input_as_lines():
        bag_type, bags_contained_list = parse_line(line)
        for _, bag_type_contained in bags_contained_list:
            bag_dict[bag_type_contained].append(bag_type)
    return bag_dict


def part1():
    # -1 for the shiny bag itself
    return len(get_all_containers(parse_contained_to_container(), SHINY_GOLD)) - 1


def part2():
    return get_n_bags_contained(parse_container_to_contained(), SHINY_GOLD)


if __name__ == '__main__':
    print(part1())
    print(part2())
