#! /usr/bin/env python3

"""
Each allergen is in exactly one ingredient
Each ingredient contains exactly 0 or 1 allergens
Allergens are not always marked

Part 1: Determine which ingredients can not contain any allergens

we KNOW that if an allergen shows up, one of the ingredients MUST contain that allergen
so every time an allergen shows up, its ingredient must be there


"""


def read(fname):
    with open(fname, "r") as f:
        dat = f.read().split("\n")

    all_ingredients = []
    allergen_to_possible_ingredients = dict()
    for line in dat:
        if line == "":
            continue
        raw_ingredients, raw_allergens = line.split(" (")

        ingredients = set(raw_ingredients.split(" "))
        allergens = raw_allergens.replace("contains ", "").replace(")", "").split(", ")

        all_ingredients.extend(list(ingredients))

        # right now, we are pre loading the allergen_to_possible_ingredients sets
        # with the first found ingredients for each allergen; then, for each subsequent
        # time that the allergen occurs, we intersect it's set with the list of ingredients
        # since there is 1 allergen to 1 ingredient, and since if an allergen is present, its
        # ingredient is certainly there, then after intersecting with all other ingredients,
        # we (should) have a shortened list of all ingredients
        for allergen in allergens:
            if allergen not in allergen_to_possible_ingredients:
                allergen_to_possible_ingredients[allergen] = ingredients.copy()
            else:
                allergen_to_possible_ingredients[allergen].intersection_update(
                    ingredients
                )

    return allergen_to_possible_ingredients, all_ingredients


def reduce_atpi(allergen_to_possible_ingredients):
    has_allergen = set()
    while True:
        no_change = True
        for k, v in allergen_to_possible_ingredients.items():
            if len(v) == 1:
                has_allergen.update(v)
            else:
                v.difference_update(has_allergen)
                no_change = False
        if no_change:
            break
    return has_allergen


def p1(fname):
    allergen_to_possible_ingredients, ingredients = read(fname)
    has_allergen = reduce_atpi(allergen_to_possible_ingredients)
    unique_ingredients = set(ingredients)
    return sum([ingredients.count(ing) for ing in unique_ingredients - has_allergen])


def p2(fname):
    allergen_to_possible_ingredients, ingredients = read(fname)
    has_allergen = reduce_atpi(allergen_to_possible_ingredients)
    return ",".join(
        [
            v[1].pop()
            for v in sorted(
                list(allergen_to_possible_ingredients.items()), key=lambda v: v[0]
            )
        ]
    )


print(p1("input.txt"))
print(p2("input.txt"))
