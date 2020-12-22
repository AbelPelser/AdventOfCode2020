from typing import List

from util import mult, read_input, safe_split


def field_matches_rules(field, rules):
    return any(rule[0] <= field <= rule[1] for rule in rules)


def field_matches_any_rule(field, field_rules):
    return any(field_matches_rules(field, rules) for rules in field_rules.values())


def get_error_rate(ticket, field_rules):
    return sum(field for field in ticket if not field_matches_any_rule(field, field_rules))


def ticket_is_valid(ticket, field_rules):
    return all(field_matches_any_rule(field, field_rules) for field in ticket)


def find_possible_fields(field_value, field_rules):
    return {field for field, rules in field_rules.items()
            if field_matches_rules(field_value, rules)}


class Position:
    def __init__(self, index: int):
        self.index = index
        self.possible_fields: List[Field] = list()


class Field:
    def __init__(self, name: str):
        self.name = name
        self.possible_positions: List[Position] = list()


def find_field_positions(positions: List[Position], field_names: List[Field]):
    locations_per_field = dict()

    def link_field_to_position(mapped_f, mapped_p):
        if mapped_f.name not in locations_per_field.keys():
            locations_per_field[mapped_f.name] = mapped_p.index
            for p in [p for p in mapped_f.possible_positions if p != mapped_p]:
                p.possible_fields.remove(mapped_f)
            for f in [f for f in mapped_p.possible_fields if f != mapped_f]:
                f.possible_positions.remove(mapped_p)
            mapped_f.possible_positions = [mapped_p]
            mapped_p.possible_fields = [mapped_f]

    while not all(map(lambda p: len(p.possible_fields) == 1, positions)):
        for position in positions:
            if len(position.possible_fields) == 1:
                link_field_to_position(position.possible_fields[0], position)
        for field in field_names:
            if len(field.possible_positions) == 1:
                link_field_to_position(field, field.possible_positions[0])
    return locations_per_field


def parse_input(text):
    rule_lines, your_ticket_lines, nearby_ticket_lines = map(lambda t: safe_split(t, '\n'), safe_split(text, '\n\n'))
    return parse_rules(rule_lines), \
           parse_ticket(your_ticket_lines[-1]), \
           list(map(parse_ticket, nearby_ticket_lines[1:]))


def parse_rules(rule_lines):
    field_rules = dict()
    for line in rule_lines:
        name, rules = line.split(':')
        rules = [rule.strip().split('-') for rule in rules.split(' or ')]
        for i in range(len(rules)):
            rules[i] = (int(rules[i][0]), int(rules[i][1]))
        field_rules[name] = rules
    return field_rules


def parse_ticket(ticket_line):
    return list(map(int, safe_split(ticket_line, ',')))


def part1():
    field_rules, _, nearby_tickets = parse_input(read_input())
    return sum(get_error_rate(t, field_rules) for t in nearby_tickets)


def part2():
    field_rules, your_ticket, nearby_tickets = parse_input(read_input())

    valid_tickets = list(filter(lambda t: ticket_is_valid(t, field_rules), nearby_tickets))

    fields = {field_name: Field(field_name) for field_name in field_rules.keys()}
    positions: List[Position] = [Position(i) for i in range(len(fields))]

    for position in positions:
        possible_fieldnames_str = set.intersection(
            *(find_possible_fields(t[position.index], field_rules)
              for t in valid_tickets))
        position.possible_fields = [fields[field_name] for field_name in possible_fieldnames_str]

    for field_name in fields.values():
        field_name.possible_positions = list(filter(lambda p: field_name in p.possible_fields, positions))
    location_per_fieldname = find_field_positions(positions, list(fields.values()))
    return mult(your_ticket[location_per_fieldname[f]]
                for f in location_per_fieldname.keys() if f.startswith('departure'))


if __name__ == '__main__':
    print(part1())
    print(part2())
