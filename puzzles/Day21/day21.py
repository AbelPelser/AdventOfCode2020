import pprint
from collections import defaultdict

from util import read_input_as_lines

if __name__ == '__main__':
    lines = read_input_as_lines()
    # lines = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)""".split('\n')
    allergens_per_ingredient = defaultdict(list)
    ingredients_per_allergen = defaultdict(set)
    all_ingredients = []
    for line in lines:
        ingredients_list = line.split('(contains')[0].strip().split(' ')
        all_ingredients += ingredients_list
        ingredients_set = set(ingredients_list)
        allergens_list = line.split('(contains')[-1].strip()[:-1].split(', ')
        for ingredient in ingredients_list:
            allergens_per_ingredient[ingredient] += allergens_list
        for allergen in allergens_list:
            if len(ingredients_per_allergen[allergen]) == 0:
                ingredients_per_allergen[allergen] = ingredients_set
            else:
                ingredients_per_allergen[allergen] = set.intersection(ingredients_per_allergen[allergen], ingredients_set)


    pprint.pprint(ingredients_per_allergen)


    # part 1
    all_allergic_ingredients = set.union(*ingredients_per_allergen.values())
    inert_ingredients = set()
    count = 0
    for ingredient in all_ingredients:
        if ingredient not in all_allergic_ingredients:
            inert_ingredients.add(ingredient)
            count += 1
    print(count)
    print(inert_ingredients)


    while True:
        change = False
        for allergen in ingredients_per_allergen.keys():
            if len(ingredients_per_allergen[allergen]) == 0:
                raise ValueError(pprint.pformat(ingredients_per_allergen))
            elif len(ingredients_per_allergen[allergen]) == 1:
                ingredient_match = list(ingredients_per_allergen[allergen])[0]
                for allergen_ in ingredients_per_allergen.keys():
                    if allergen_ != allergen and ingredient_match in ingredients_per_allergen[allergen_]:
                        ingredients_per_allergen[allergen_].remove(ingredient_match)
                        change = True
        if not change:
            break
    pprint.pprint(ingredients_per_allergen)

    for val in ingredients_per_allergen.values():
        assert len(val) == 1

    a = [(key, list(val)[0]) for key, val in ingredients_per_allergen.items()]
    a = sorted(a, key=lambda t: t[0])
    print(a)
    print(','.join([t[1] for t in a]))