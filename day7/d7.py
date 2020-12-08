#! /usr/bin/env python3

from typing import Dict, List, Set


def part1():
    Bag = str
    with open("input.txt", "r") as f:

        bag_held_in: Dict[Bag, List[Bag]] = dict()

        for line in f.readlines():
            # remove "formatting" words
            line = (
                line.replace("no other bags", "")
                .replace(" bags", "")
                .replace(" bag", "")
            )

            # split into parent and child bags
            super_bag, b = line.split(" contain ")
            bag_colors_it_holds = [
                g[2:] for g in b.replace(".\n", "").split(", ") if g != "no other bags"
            ]  # first 2 chars are num and a space

            # set map of bag to the bags that hold it
            for bag in bag_colors_it_holds:
                if bag not in bag_held_in:
                    bag_held_in[bag] = [super_bag]
                else:
                    bag_held_in[bag].append(super_bag)

        # calculate number of color classes
        s = 0
        seen = set()
        to_see = set(bag_held_in["shiny gold"])
        while len(to_see) > 0:
            bag = to_see.pop()
            if bag not in seen:
                s += 1
                seen.add(bag)

            if bag not in bag_held_in:
                # bag isnt held in any other bag
                continue

            # add parents to the set we need to attend to
            to_see = to_see.union(set(bag_held_in[bag]))

        return s


def part2():
    Bag = str
    with open("input.txt", "r") as f:

        bag_holds: Dict[Bag, List[Bag]] = dict()

        for line in f.readlines():
            line = (
                line.replace("no other bags", "")
                .replace(" bags", "")
                .replace(" bag", "")
                .replace(".\n", "")
            )
            super_bag, b = line.split(" contain ")

            bag_nums_it_holds = b.split(", ")
            if bag_nums_it_holds != [""]:
                bag_holds[super_bag] = [
                    (int(g[:2]), g[2:])
                    for g in bag_nums_it_holds
                    if g != "no other bags"
                ]  # first 2 chars are num and a space

        def f(n_b):
            if n_b[1] not in bag_holds:
                return n_b[0]
            s = 0
            for child_n_b in bag_holds[n_b[1]]:
                s += n_b[0] * f(child_n_b)
            return s + n_b[0]

        return f((1, "shiny gold")) - 1


print(part1())
print(part2())
