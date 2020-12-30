#! /usr/bin/env python3

from __future__ import annotations


test_input = [int(v) for v in list(str(389125467))]
real_input = [int(v) for v in list(str(712643589))]


""" Move

1. Remove next three cups that are immediately clockwise of current cup
2. Select destination cup (cup with a label equal tot he current cup's label minus 1.
   If this would select one of the cups that was just picked up, the crab will keep
   subtracting one until it finds a cup that wasnt picket up.
   If at any point the value goes below the lowest value label, it wraps around to highest
   value label
3. Place the 3 removed cups immediately clockwise of the destination cup, maintaining the
   same pick-up order.
4. Select a new current cup, which is immediately clockwise of the current cup
"""


def move_slow(c, current):
    def _get(arr, idx):
        try:
            return arr.index(idx)
        except ValueError:
            return None

    idx = c.index(current)

    if idx > len(c):
        raise RuntimeError(f"current cup idx {idx} out of list range")

    if idx + 3 < len(c):
        rem = c[idx + 1 : idx + 4]
        del c[idx + 1 : idx + 4]
    else:
        lower = min(idx + 1, len(c))
        upper = idx + 4 - len(c)
        rem = c[lower:] + c[:upper]
        del c[lower:]
        del c[:upper]

    destination = current - 1
    while (destination_idx := _get(c, destination)) is None:
        if destination < 1:
            destination = 1000000
        else:
            destination -= 1

    new = c[: destination_idx + 1] + rem + c[destination_idx + 1 :]
    next_val = (
        new[new.index(current) + 1] if new.index(current) != len(new) - 1 else new[0]
    )

    return new, next_val


class Node:
    def __init__(self, value: int, nxt: Node = None, prv: Node = None):
        self.value = value
        self.nxt = nxt
        self.prv = prv

    def __repr__(self):
        nxt = None if self.nxt is None else self.nxt.value
        prv = None if self.prv is None else self.prv.value
        return f"<prv:{prv} this:{self.value} nxt:{nxt}>"

    def copy(self):
        return Node(self.value, self.nxt, self.prv)


def find(node, value, reverse=False):
    s = set()
    while node.value not in s:
        if node.value == value:
            return node
        s.add(node.value)
        node = node.prv if reverse else node.nxt
    raise RuntimeError("Could not find value")


def move(curr_node):
    """
    linkedlist!

    cd is a dualdict from index to value
    idx is the index of the current val
    """
    popped = remove_3_after(curr_node)


def insert_chain_after(curr_node, chain):
    split_after = curr_node.nxt

    end_of_chain = chain.prv
    split_after.prv = end_of_chain
    end_of_chain.nxt = split_after

    chain.prv = curr_node
    curr_node.nxt = chain

    return curr_node


def remove_3_after(curr_node):
    start_of_removed = curr_node.nxt
    end_of_removed = curr_node.nxt.nxt.nxt
    after_end = curr_node.nxt.nxt.nxt.nxt

    curr_node.nxt = after_end
    start_of_removed.prv = end_of_removed

    end_of_removed.nxt = start_of_removed
    after_end.prv = curr_node
    return start_of_removed


def iterate(node):
    n = node
    while True:
        yield n
        n = n.nxt


def print_chain(node):
    a_s = set()
    for x in iterate(node):
        if x is None:
            break
        if x.value in a_s:
            break
        print(x)
        a_s.add(x.value)


def construct_DLL(values):
    zeroth_node = Node(values[0])
    prev_node = zeroth_node
    for v in values[1:]:
        curr_node = Node(v, prv=prev_node)
        prev_node.nxt = curr_node
        prev_node = curr_node

    prev_node.nxt = zeroth_node
    zeroth_node.prv = prev_node
    return zeroth_node


def p1(inp):
    a, idx = inp, inp[0]
    for _ in range(100):
        a, idx = move_slow(a, idx)
    return a


def p2(inp):
    a = inp + [i for i in range(10, 1000001)]
    current = construct_LL(a)
    for _ in range(10000000):
        current = move(current)

    # todo do these
    ind_1 = a.index(1)
    return a[ind_1 + 1] * a[ind_1 + 2]


if __name__ == "__main__":
    a = construct_LL(list(range(25)))
    start = move(a)

    print_chain(a)
    print()
    print_chain(start)

# print(p1(real_input))
# print(p2(real_input))
