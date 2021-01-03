import re

from util import read_input_as_lines


def part1():
    possible_ingredients_per_allergen, all_ingredient_mentions = parse_input(read_input_as_lines())
    all_allergic_ingredients = set.union(*possible_ingredients_per_allergen.values())
    return len(list(i for i in all_ingredient_mentions if i not in all_allergic_ingredients))


def part2():
    possible_ingredients_per_allergen, _ = parse_input(read_input_as_lines())
    ingredients_per_allergen = {}
    while len(ingredients_per_allergen) < len(possible_ingredients_per_allergen):
        for allergen in possible_ingredients_per_allergen.keys():
            if len(possible_ingredients_per_allergen[allergen]) == 1:
                ingredient = possible_ingredients_per_allergen[allergen].pop()
                ingredients_per_allergen[allergen] = ingredient
                for ingredient_list in possible_ingredients_per_allergen.values():
                    ingredient_list.discard(ingredient)
    return ','.join([i for _, i in sorted(ingredients_per_allergen.items())])


def parse_input(lines):
    possible_ingredients_per_allergen = dict()
    all_ingredient_mentions = []
    for line in lines:
        ingredients, allergens = re.match('([a-z ]+) \\(contains ([a-z ,]+)\\)', line).groups()

        ingredients_list = ingredients.split(' ')
        ingredients_set = set(ingredients_list)
        all_ingredient_mentions += ingredients_list
        for allergen in allergens.split(', '):
            if allergen not in possible_ingredients_per_allergen.keys():
                possible_ingredients_per_allergen[allergen] = ingredients_set
            else:
                possible_ingredients_per_allergen[allergen] = ingredients_set.intersection(
                    possible_ingredients_per_allergen[allergen])

    return possible_ingredients_per_allergen, all_ingredient_mentions


if __name__ == '__main__':
    lines = read_input_as_lines()
    print(part1())
    print(part2())
