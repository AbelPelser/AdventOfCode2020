import re

from util import read_input, safe_split

REGEX_GROUP_MAX = 6


def parse_rules(rule_lines):
    direct_rules = dict()
    indirect_rules = dict()

    for line in rule_lines:
        rule_nr, rule = line.split(':')
        rule_nr = int(rule_nr)
        rule = rule.strip()
        if "\"" in rule:
            rule = rule.replace("\"", "")
            direct_rules[rule_nr] = rule
        else:
            indirect_rules[rule_nr] = [list(map(int, sub_rule.strip().split(' '))) for sub_rule in rule.split('|')]
    return direct_rules, indirect_rules


class RuleRegexGeneratorPart1:
    def rule_to_regex(self, direct_rules, indirect_rules, rule_nr):
        if rule_nr in direct_rules.keys():
            return direct_rules[rule_nr]
        else:
            sub_rules = []
            for sub_rule in indirect_rules[rule_nr]:
                sub_rules.append(''.join(self.rule_to_regex(direct_rules, indirect_rules, sub_rule_nr)
                                         for sub_rule_nr in sub_rule))
            return '(' + '|'.join(sub_rules) + ')'

    def all_rules_to_regex(self, direct_rules, indirect_rules):
        rules_to_str = {}
        for key in direct_rules.keys():
            rules_to_str[key] = '^' + self.rule_to_regex(direct_rules, indirect_rules, key) + '$'
        for key in indirect_rules.keys():
            rules_to_str[key] = '^' + self.rule_to_regex(direct_rules, indirect_rules, key) + '$'
        return rules_to_str


class RuleRegexGeneratorPart2(RuleRegexGeneratorPart1):
    named_regex_group_counter = 0

    def rule_to_regex(self, direct_rules, indirect_rules, rule_nr):
        if rule_nr == 8:
            return f'({self.rule_to_regex(direct_rules, indirect_rules, 42)})+'
        elif rule_nr == 11:
            pre_str = f'{self.rule_to_regex(direct_rules, indirect_rules, 42)}'
            post_str = f'{self.rule_to_regex(direct_rules, indirect_rules, 31)}'
            for _ in range(REGEX_GROUP_MAX):
                pre_str += f'(?P<g{self.named_regex_group_counter}>' \
                           f'{self.rule_to_regex(direct_rules, indirect_rules, 42)})?'
                post_str += f'(?(g{self.named_regex_group_counter})' \
                            f'{self.rule_to_regex(direct_rules, indirect_rules, 31)})'
                self.named_regex_group_counter += 1
            return f'({pre_str}{post_str})'
        return super().rule_to_regex(direct_rules, indirect_rules, rule_nr)


def parse_input(text):
    rule_text, msg_text = safe_split(text, '\n\n')
    direct_rules, indirect_rules = parse_rules(safe_split(rule_text, '\n'))
    return direct_rules, indirect_rules, safe_split(msg_text, '\n')


def find_n_matching_lines(regex, lines):
    return len(list(filter(lambda line: re.match(regex, line), lines)))


def part1():
    direct_rules, indirect_rules, msg_lines = parse_input(read_input())
    rules_to_regex = RuleRegexGeneratorPart1().all_rules_to_regex(direct_rules, indirect_rules)
    return find_n_matching_lines(rules_to_regex[0], msg_lines)


def part2():
    direct_rules, indirect_rules, msg_lines = parse_input(read_input())
    rules_to_regex = RuleRegexGeneratorPart2().all_rules_to_regex(direct_rules, indirect_rules)
    return find_n_matching_lines(rules_to_regex[0], msg_lines)


if __name__ == '__main__':
    print(part1())
    print(part2())
