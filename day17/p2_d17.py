#! /usr/bin/env python3


def neighbors_of(w, x, y, z, actives):
    neighbors = set()
    for l in [-1, 0, 1]:
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                for p in [-1, 0, 1]:
                    if (w + l, x + m, y + n, z + p) in actives:
                        neighbors.add((w + l, x + m, y + n, z + p))
    neighbors.discard((w, x, y, z))
    return neighbors


def get_max_bounds(actives):
    activ_iter = iter(actives)
    start = next(activ_iter)
    max_w, max_x, max_y, max_z = start[0], start[1], start[2], start[3]
    min_w, min_x, min_y, min_z = start[0], start[1], start[2], start[3]
    for active in actives:
        min_w = min(min_w, active[0])
        max_w = max(max_w, active[0])

        min_x = min(min_x, active[1])
        max_x = max(max_x, active[1])

        min_y = min(min_y, active[2])
        max_y = max(max_y, active[2])

        min_z = min(min_z, active[3])
        max_z = max(max_z, active[3])
    return (
        min_w - 2,
        max_w + 2,
        min_x - 2,
        max_x + 2,
        min_y - 2,
        max_y + 2,
        min_z - 2,
        max_z + 2,
    )


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
    min_w, max_w, min_x, max_x, min_y, max_y, min_z, max_z = get_max_bounds(actives)
    for i in range(min_w, max_w):
        for j in range(min_x, max_x):
            for k in range(min_y, max_y):
                for p in range(min_z, max_z):
                    if (i, j, k, p) not in actives:
                        neigbors = neighbors_of(i, j, k, p, actives)
                        if len(neigbors) == 3:
                            next_actives.add((i, j, k, p))

    return next_actives


def init(fname):
    with open(fname, "r") as f:
        grid = [list(row) for row in f.read().split("\n") if row != ""]

    actives = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                actives.add((i, j, 0, 0))

    return actives


def iterate(fname, num_iters):
    actives = init(fname)
    for i in range(num_iters):
        actives = chg(actives)
    return actives


actives = iterate("input.txt", 6)
print(len(actives))
