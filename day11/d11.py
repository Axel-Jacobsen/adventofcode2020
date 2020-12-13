#! /usr/bin/env python3


import numpy as np


EMPTY = "L"
FLOOR = "."
OCCUP = "#"


def print_layout(layout):
    for l in layout:
        print("".join(l.tolist()))
    print()


def chg(seat, neighbors, n_threshold):
    if seat == EMPTY and all([n == EMPTY or n == FLOOR for n in neighbors]):
        return OCCUP
    if seat == OCCUP and sum([int(n == OCCUP) for n in neighbors]) >= n_threshold:
        return EMPTY
    return seat


def get_neighbors_p1(i, j, layout):
    x_len, y_len = layout.shape
    min_x, max_x = max(0, i - 1), min(i + 2, x_len)
    min_y, max_y = max(0, j - 1), min(j + 2, y_len)
    neighbors = layout[min_x:max_x, min_y:max_y].flatten().tolist()
    neighbors.remove(layout[i, j])
    return neighbors


def get_neighbors_p2(i, j, layout):
    x_len, y_len = layout.shape

    def mv_w_steps_fm_until(dx, dy, i, j):
        cx = i + dx
        cy = j + dy
        while 0 <= cx < x_len and 0 <= cy < y_len:
            if layout[cx, cy] != FLOOR:
                return layout[cx, cy]
            cx = cx + dx
            cy = cy + dy
        return FLOOR  # unoccupied

    return [
        mv_w_steps_fm_until(*dv, i, j)
        for dv in (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        )
    ]


def step(prev_layout, next_layout, neighbor_fcn, n_threshold):
    x_len, y_len = prev_layout.shape
    for i in range(x_len):
        for j in range(y_len):
            if prev_layout[i, j] == FLOOR:
                continue
            neighbors = neighbor_fcn(i, j, prev_layout)
            next_layout[i, j] = chg(prev_layout[i, j], neighbors, n_threshold)


def iterate(neighbor_fcn, n_threshold):
    with open("input.txt", "r") as f:
        layout1 = np.asarray([list(row) for row in f.read().split("\n") if row != ""])
        layout2 = np.asarray([row[:] for row in layout1])

        step(layout1, layout2, neighbor_fcn, n_threshold)  # init step

        i = 1
        while not np.array_equal(layout1, layout2):
            if i % 2 == 0:
                step(layout1, layout2, neighbor_fcn, n_threshold)
            else:
                step(layout2, layout1, neighbor_fcn, n_threshold)
            i += 1

    return (layout1 == OCCUP).astype(int).sum()


print(iterate(get_neighbors_p1, 4))
print(iterate(get_neighbors_p2, 5))
