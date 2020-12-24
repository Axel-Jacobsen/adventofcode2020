#! /usr/bin/env python3

import numpy as np

from collections import defaultdict


class TileEdgeMatch(object):
    def __init__(self, tn1: int, tn2: int, t1_edge_code: str, t2_edge_code: str):
        self.tn1 = tn1
        self.tn2 = tn2
        self.t1_edge_code = t1_edge_code
        self.t2_edge_code = t2_edge_code

    def __repr__(self):
        return f"<TEM ({self.tn1}, {self.t1_edge_code})<->({self.tn2}, {self.t2_edge_code})>"

    def __hash__(self):
        tns = [str(s) for s in sorted([self.tn1, self.tn2])]
        edge_codes = ["t", "b", "l", "r", "tf", "bf", "lf", "rf"]
        edges = sorted(
            [str(edge_codes.index(e)) for e in [self.t1_edge_code, self.t2_edge_code]]
        )
        return int(f"{''.join(tns)}{''.join(edges)}")

    def __eq__(self, x):
        if not isinstance(x, self.__class__):
            return False
        return self.__hash__() == x.__hash__()

    def __ne__(self, x):
        return not self.__eq__(x)


def get_tiles(fname):
    tiles = {}
    with open(fname, "r") as f:
        dat = f.read().split("\n\n")
        for tile in dat:
            lines = tile.split("\n")
            tile_num = int(lines[0].replace("Tile ", "").replace(":", ""))
            tile_arr = np.asarray([list(l) for l in lines[1:] if l != ""])
            tiles[tile_num] = tile_arr
    return tiles


def get_tile_edges(t):
    """
    Return only the possible edges that can be chosen
    Confirm that we do not have to do further checking that
    we are not setting a flipped to flip

    t -> top
    b -> bottom
    l -> left
    r -> right
    tf -> top, LR Flipped
    bf -> bottom, LR Flipped
    lf -> left, TD Flipped
    rf -> right, TD Flipped
    """
    return [
        (t[0, :], "t"),
        (t[-1, :], "b"),
        (t[:, 0], "l"),
        (t[:, -1], "r"),
        (np.flip(t[0, :]), "tf"),
        (np.flip(t[-1, :]), "bf"),
        (np.flip(t[:, 0]), "lf"),
        (np.flip(t[:, -1]), "rf"),
    ]


def get_matching_edge_code(edge, edge_list):
    match = [(edge == v[0]).all() for v in edge_list]
    return edge_list[match.index(True)][1] if True in match else None


def get_tcs_by_num(num, tile_connections):
    s = set()
    for tc in tile_connections:
        if tc.tn1 == num or tc.tn2 == num:
            s.add(tc)
    return s


def get_tcs_by_pair(num1, num2, tile_connections):
    return get_tcs_by_num(num1, get_tcs_by_num(num2, tile_connections))


def get_tile_connections(tiles):
    tile_connections = set()
    for tn1, t1 in tiles.items():
        for tn2, t2 in tiles.items():
            if tn1 == tn2:
                continue

            t1_edges = get_tile_edges(t1)
            t2_edges = get_tile_edges(t2)

            for t1_edge, t1_edge_code in t1_edges:
                t2_edge_code = get_matching_edge_code(t1_edge, t2_edges)

                if t2_edge_code is not None:
                    tile_connections.add(
                        TileEdgeMatch(tn1, tn2, t1_edge_code, t2_edge_code)
                    )
    return tile_connections


def p1(fname):
    tiles = get_tiles(fname)
    tile_connections = get_tile_connections(tiles)

    d = defaultdict(int)

    for tc in tile_connections:
        d[tc.tn1] += 1
        d[tc.tn2] += 1

    img_height_b, img_width_b = tiles[next(iter(tiles))].shape

    img_height = img_height_b - 2
    img_width = img_width_b - 2

    # for tem in tile_connections:
        pass

    p = 1
    for k, v in d.items():
        if v == 3 or v == 4:
            p *= k

    return p


def p2(fname):
    tiles = get_tiles(fname)
    tile_connections = get_tile_connections(tiles)


print(p1("test_input.txt"))
