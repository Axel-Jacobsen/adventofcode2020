#! /usr/bin/env python3


import numpy as np


class Tile:
    def __init__(self, tile_num, tile):
        self.tile_num = tile_num
        self.tarr = tile
        # 0 = top, 1 = right, 2 = bottom, 3 = left
        self.neighbors = {i: None for i in range(4)}
        self.lr_flip = False
        self.td_flip = False


def get_tiles(fname):
    tiles = {}
    with open(fname, "r") as f:
        dat = f.read().split("\n\n")
        for tile in dat:
            lines = tile.split("\n")
            tile_num = int(lines[0].replace("Tile ", "").replace(":", ""))
            tile_arr = np.asarray([list(l) for l in lines[1:] if l != ""])
            tiles[tile_num] = Tile(tile_num, tile_arr)
    return tiles


def get_tile_edges(t):
    return (
        t[0, :],
        t[:, -1],
        t[-1, :],
        t[:, 0],
        np.flip(t[0, :]),
        np.flip(t[:, -1]),
        np.flip(t[-1, :]),
        np.flip(t[:, 0]),
    )


def get_matching_idx(edge, edge_list):
    match = [(edge == v).all() for v in edge_list]
    return match.index(True) if True in match else None


def construct_img(tiles):
    placed = 0

    while placed < len(tiles):
        for tn1, t1 in tiles.items():
            for tn2, t2 in tiles.items():
                if tn1 == tn2 or tn1 in t2.neighbors.values():
                    continue

                t2_edges = get_tile_edges(t2.tarr)
                for t1_edge in get_tile_edges(t1.tarr):
                    if (idx := get_matching_idx(t1_edge, t2_edges)) is not None:
                        if idx > 3:
                            # t2 must be flipped for the match to take place
                            print(f"tn1 {tn1} reqs flip for tn2 {tn2} idx {idx}")
                            if idx == 4:
                                t1.lr_flip = True

                            idx -= 4

                        t2.neighbors[idx] = tn1
                        # set tn1 negihbor to oposite side of tn2
                        if idx < 2:
                            assert (
                                idx == 0 or idx == 1
                            ), f"expected idx == 3 or idx == 4, got idx == {idx}"
                            t1.neighbors[idx + 2] = tn2
                        else:
                            assert (
                                idx == 2 or idx == 3
                            ), f"expected idx == 3 or idx == 4, got idx == {idx}"
                            t1.neighbors[idx - 2] = tn2
                        placed += 1


tiles = get_tiles("input.txt")
construct_img(tiles)
p = 1
for tn, tile in tiles.items():
    print(tn, tile.neighbors)
    if list(tile.neighbors.values()).count(None) == 2:
        print('\t', tn)
        p *= tn
print(p)
