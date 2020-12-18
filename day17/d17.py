#! /usr/bin/env python3


def neighbors_of(i, j, k, actives):
    neighbors = set()
    for l in [-1, 0, 1]:
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                if (i + l, j + m, k + n) in actives:
                    neighbors.add((i + l, j + m, k + n))
    neighbors.discard((i, j, k))
    return neighbors


def get_max_bounds(actives):
    activ_iter = iter(actives)
    start = next(activ_iter)
    max_x, max_y, max_z = start[0], start[1], start[2]
    min_x, min_y, min_z = start[0], start[1], start[2]
    for active in actives:
        min_x = min(min_x, active[0])
        max_x = max(max_x, active[0])

        min_y = min(min_y, active[1])
        max_y = max(max_y, active[1])

        min_z = min(min_z, active[2])
        max_z = max(max_z, active[2])

    return min_x - 5, max_x + 5, min_y - 5, max_y + 5, min_z - 5, max_z + 5


def chg(actives):
    """
    If a cube is active and exactly 2 or 3 of its neighbors are
    also active, the cube remains active. Otherwise, the cube becomes inactive.

    If a cube is inactive but exactly 3 of its neighbors are active,
    the cube becomes active. Otherwise, the cube remains inactive.
    """
    # deal with all current actives
    next_actives = set()
    for actv in actives:
        neighbors = neighbors_of(*actv, actives)
        if len(neighbors) == 2 or len(neighbors) == 3:
            next_actives.add(actv)

    # How to deal with inactives -> actives?
    # Get "max bounds" for cube, and for every inactive cube,
    # get neighbors etc etc
    min_x, max_x, min_y, max_y, min_z, max_z = get_max_bounds(actives)
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            for k in range(min_z, max_z):
                if (i, j, k) not in actives:
                    neigbors = neighbors_of(i, j, k, actives)
                    if len(neigbors) == 3:
                        next_actives.add((i, j, k))

    return next_actives


def init(fname):
    with open(fname, "r") as f:
        grid = [list(row) for row in f.read().split("\n") if row != ""]

    actives = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                actives.add((i, j, 0))

    return actives


def iterate(fname, num_iters):
    actives = init(fname)
    for i in range(num_iters):
        actives = chg(actives)
    return actives


actives = iterate("input.txt", 6)
print(len(actives))
