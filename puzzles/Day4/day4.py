import re
from typing import Dict

from util import read_input_as_passports


class Field(object):
    def __init__(self, validator, optional=False):
        self.validator = validator
        self.optional = optional
        self.value = None

    def is_valid_part1(self):
        return self.value or self.optional

    def is_valid_part2(self):
        return self.optional if not self.value else self.validator(self.value)


class HeightField(Field):
    def __init__(self):
        super().__init__(HeightField.validate)

    @staticmethod
    def validate(v):
        if re.match('[0-9]{2}in', v):
            return 59 <= int(v[:-2]) <= 76
        elif re.match('[0-9]{3}cm', v):
            return 150 <= int(v[:-2]) <= 193
        return False


class Passport(object):
    def __init__(self, passport_str):
        self.fields: Dict[str, Field] = {
            'byr': Field(lambda v: 1920 <= int(v) <= 2002),
            'iyr': Field(lambda v: 2010 <= int(v) <= 2020),
            'eyr': Field(lambda v: 2020 <= int(v) <= 2030),
            'hgt': HeightField(),
            'hcl': Field(lambda v: re.match('^#[a-f0-9]{6}', v)),
            'ecl': Field(lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']),
            'pid': Field(lambda v: re.match('^[0-9]{9}$', v)),
            'cid': Field(lambda _: True, optional=True)
        }
        for kv_pair in re.split('\\s', passport_str):
            key, value = kv_pair.split(':')
            if key in self.fields.keys():
                self.fields[key].value = value
            else:
                print(f'INVALID KEY: {key}')

    def validate_part1(self):
        return all(field.is_valid_part1() for field in self.fields.values())

    def validate_part2(self):
        return all(field.is_valid_part2() for field in self.fields.values())


def part1():
    return sum(int(Passport(p).validate_part1()) for p in read_input_as_passports())


def part2():
    return sum(int(Passport(p).validate_part2()) for p in read_input_as_passports())


if __name__ == '__main__':
    print(part1())
    print(part2())
