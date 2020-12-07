#! /usr/bin/env python3

# < 322

# swear makes my developing faster
from typing import Dict, List, Set


Bag = str


with open("input.txt", "r") as f:

    bag_held_in: Dict[Bag, List[Bag]] = dict()

    for line in f.readlines():
        line = line.replace("no other bags", "").replace(" bags", "").replace(" bag", "")
        super_bag, b = line.split(" contain ")

        bags_it_holds = b.replace(".\n", "").split(", ")
        bag_colors_it_holds = [
            g[2:] for g in bags_it_holds if g != "no other bags"
        ]  # first 2 chars are num and a space

        for bag in bag_colors_it_holds:
            if bag not in bag_held_in.keys():
                bag_held_in[bag] = [super_bag]
            else:
                bag_held_in[bag].append(super_bag)

    s = 0
    seen = set()
    to_see = set(bag_held_in["shiny gold"])
    while len(to_see) > 0:
        bag = to_see.pop()
        if bag not in seen:
            s += 1
            seen.add(bag)
        if bag not in bag_held_in.keys():
            continue
        to_see = to_see.union(set(bag_held_in[bag]))
    print(s)
