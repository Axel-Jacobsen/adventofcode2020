#! /usr/bin/env python3


def g(data, dx, dy):
    trees = 0
    x = 0
    y = 0
    for y in range(0, len(data), dy):
        treeline = data[y]
        if treeline[x % len(treeline)] == "#":
            trees += 1
        x += dx

    return trees


with open("input.txt", "r") as f:
    data = []
    for line in f.readlines():
        data.append(list(line.strip()))

    p = 1
    dxs = [1, 3, 5, 7, 1]
    dys = [1, 1, 1, 1, 2]
    for dx, dy in zip(dxs, dys):
        p *= g(data, dx, dy)

    print(p)
