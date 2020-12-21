#! /usr/bin/env python3


import numpy as np


class Tile:
    """
    lr_flip and td_flip flag whether this Tile has been flipped along either axis
    fix_lr_flip and fix_td_flip fixes the current flip state - once set to True,
    lr_flip and td_flip can not be modified.
    """

    def __init__(self, tile_num, tile):
        self.tile_num = tile_num
        self.tarr = tile
        # 0 = top, 1 = right, 2 = bottom, 3 = left
        self.neighbors = {i: None for i in ["t", "d", "l", "r"]}
        self.lr_flip = False
        self.td_flip = False
        self.fix_lr_flip = False
        self.fix_td_flip = False

    def __repr__(self):
        return f"{self.tile_num} flips: {self.lr_flip}, {self.td_flip} fix: {self.fix_lr_flip}, {self.fix_td_flip}"

    def set_td(self):
        if not self.fix_td_flip:
            self.td_flip = True
            self.fix_td_flip = True

    def set_lr(self):
        if not self.fix_lr_flip:
            self.lr_flip = True
            self.fix_lr_flip = True

    def fix_td(self):
        self.fix_td_flip = True

    def fix_lr(self):
        self.fix_lr_flip = True

    def unfix_td(self):
        self.fix_td_flip = False

    def unfix_lr(self):
        self.fix_lr_flip = False

    def get_tile_edges(self):
        """
        Return only the possible edges that can be chosen
        Confirm that we do not have to do further checking that
        we are not setting a flipped to flip
        """
        t = self.tarr
        ret = []

        if self.fix_lr_flip:
            if not self.lr_flip:
                ret.append((t[0, :], "t"))
                ret.append((t[-1, :], "b"))
            else:
                ret.append((np.flip(t[0, :]), "tf"))
                ret.append((np.flip(t[-1, :]), "df"))
        else:
            ret.append((t[0, :], "t"))
            ret.append((t[-1, :], "b"))
            ret.append((np.flip(t[0, :]), "tf"))
            ret.append((np.flip(t[-1, :]), "df"))

        if self.fix_td_flip:
            if not self.td_flip:
                ret.append((t[:, 0], "l"))
                ret.append((t[:, -1], "r"))
            else:
                ret.append((np.flip(t[:, 0]), "lf"))
                ret.append((np.flip(t[:, -1]), "rf"))
        else:
            ret.append((t[:, 0], "l"))
            ret.append((t[:, -1], "r"))
            ret.append((np.flip(t[:, 0]), "lf"))
            ret.append((np.flip(t[:, -1]), "rf"))

        return ret


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


def get_matching_idx(edge, edge_list):
    match = [(edge[0] == v[0]).all() for v in edge_list]
    return (edge[1], edge_list[match.index(True)][1]) if True in match else None


def set_Tile(idx, num, tile):
    """
    idx is the code below which relates tile to the other tile_num "num"
    """
    td = ["t", "d"]
    lr = ["l", "r"]
    flip_td = ["tf", "df"]
    flip_lr = ["lf", "rf"]

    if idx in td:
        if tile.td_flip and not tile.fix_td_flip:
            raise RuntimeError("God!")
        tile.fix_td()
        tile.neighbors[idx] = num

    elif idx in lr:
        if tile.lr_flip and not tile.fix_lr_flip:
            raise RuntimeError("God!")
        tile.fix_lr()
        tile.neighbors[idx] = tile.tile_num

    elif idx in flip_td:
        if not tile.td_flip and tile.fix_td_flip:
            raise RuntimeError("God!")

        if not tile.fix_td_flip:
            tile.set_td()
            tile.fix_td()
        idx = idx.replace("f", "")
        tile.neighbors[idx] = num

    elif idx in flip_lr:
        if tile.lr_flip and not tile.fix_lr_flip:
            raise RuntimeError("God!")

        if not tile.fix_lr_flip:
            tile.set_lr()
            tile.fix_lr()
        idx = idx.replace("f", "")
        tile.neighbors[idx] = tile.tile_num


def construct_img(tiles):
    placed = 0

    while placed < len(tiles):
        for tn1, t1 in tiles.items():
            for tn2, t2 in tiles.items():
                if tn1 == tn2:
                    continue

                t2_edges = t2.get_tile_edges()
                for t1_edge in t1.get_tile_edges():
                    if (idxs := get_matching_idx(t1_edge, t2_edges)) is not None:
                        set_Tile(idxs[0], t2.tile_num, t1)
                        set_Tile(idxs[1], t1.tile_num, t2)
                        placed += 1


tiles = get_tiles("test_input.txt")
construct_img(tiles)
p = 1
for tn, tile in tiles.items():
    print(tile, tile.neighbors)
    if list(tile.neighbors.values()).count(None) == 2:
        print("\t", tn)
        p *= tn
print(p)
