#! /usr/bin/env python3


import functools
import itertools
import cProfile
import numpy as np


def load(fname):
    with open(fname, "r") as f:
        return [l for l in f.read().split("\n") if l != ""]


def _get_dirs(line):
    dirs = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "n" or c == "s" and line[i + 1] in "ew":
            c += line[i + 1]
            i += 1
        i += 1
        dirs.append(c)
    return dirs


def get_loc(line):
    dir_vec = {
        "nw": np.asarray([0, 1, -1]),
        "ne": np.asarray([1, 0, -1]),
        "sw": np.asarray([-1, 0, 1]),
        "se": np.asarray([0, -1, 1]),
        "w": np.asarray([-1, 1, 0]),
        "e": np.asarray([1, -1, 0]),
    }
    dirs = _get_dirs(line)
    loc = np.zeros(3)
    for d in dirs:
        loc += dir_vec[d]
    return tuple(loc)


def get_black_tiles(fname):
    dat = load(fname)
    s = set()
    for line in dat:
        if (x := get_loc(line)) in s:
            s.remove(x)
        else:
            s.add(x)
    return s


####### Copy-Pasted and modified fm. d17p1
dirs = [
    np.asarray([0, 1, -1]),
    np.asarray([1, 0, -1]),
    np.asarray([-1, 0, 1]),
    np.asarray([0, -1, 1]),
    np.asarray([-1, 1, 0]),
    np.asarray([1, -1, 0]),
]


@functools.cache
def _neighbors_of(i, j, k):
    return {(i + l, j + m, k + n) for l,m,n in dirs}

def neighbors_of(i, j, k, black_tiles):
    n = _neighbors_of(i,j,k)
    return black_tiles.intersection(n)

def get_max_bounds(black_tiles):
    activ_iter = iter(black_tiles)
    start = next(activ_iter)
    max_x, max_y, max_z = start[0], start[1], start[2]
    min_x, min_y, min_z = start[0], start[1], start[2]
    for active in black_tiles:
        min_x = min(min_x, active[0])
        max_x = max(max_x, active[0])
        min_y = min(min_y, active[1])
        max_y = max(max_y, active[1])
        min_z = min(min_z, active[2])
        max_z = max(max_z, active[2])

    return (
        int(min_x) - 2,
        int(max_x) + 2,
        int(min_y) - 2,
        int(max_y) + 2,
        int(min_z) - 2,
        int(max_z) + 2,
    )


def chg(black_tiles):
    """
    If a cube is active and exactly 2 or 3 of its neighbors are
    also active, the cube remains active. Otherwise, the cube becomes inactive.

    If a cube is inactive but exactly 3 of its neighbors are active,
    the cube becomes active. Otherwise, the cube remains inactive.
    """
    next_black_tiles = set()
    for actv in black_tiles:
        neighbors = neighbors_of(*actv, black_tiles)
        if len(neighbors) in [1, 2]:
            next_black_tiles.add(actv)

    min_x, max_x, min_y, max_y, min_z, max_z = get_max_bounds(black_tiles)
    all_possible_flips = set(
        itertools.product(range(min_x, max_x), range(min_y, max_y), range(min_z, max_z))
    )
    for (i,j,k) in all_possible_flips - black_tiles:
        neigbors = neighbors_of(i, j, k, black_tiles)
        if len(neigbors) == 2:
            next_black_tiles.add((i, j, k))
    return next_black_tiles


####### Copy Pasted fm. d17p1


def p1(fname):
    return len(get_black_tiles(fname))


def p2(fname):
    """
    black tile with zero or more than 2 -> white
    white tile with exactly 2 black tiles immediately adjacent to it -> black.
    """
    black_tiles = get_black_tiles(fname)
    for _ in range(100):
        print(_, len(black_tiles))
        black_tiles = chg(black_tiles)

    print(len(black_tiles))


print(p1("input.txt"))
print(p2("input.txt"))
# cProfile.run("p2('test_input.txt')")
