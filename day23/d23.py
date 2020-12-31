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

solving p2 with DLL and value-node map gives an answer in ~31 seconds
"""


def move(curr_node, max=10000000, v_n: dict = None):
    # - curr_node is in the double-linked-list (DLL)
    # - v_n is a dict of values to nodes with those values,
    # - max is the maximum value in the DLL, so we don't have to search
    #   for the max value each time

    popped = remove_3_after(curr_node)
    popped_values = get_value_set(popped)

    next_destination_val = curr_node.value - 1
    if next_destination_val < 1:
        next_destination_val = max

    while next_destination_val in popped_values:
        v = next_destination_val - 1
        next_destination_val = max if v < 1 else v

    next_destination = v_n[next_destination_val]
    insert_chain_after(next_destination, popped)
    return curr_node.nxt


class Node:
    def __init__(self, value: int, nxt: Node = None, prv: Node = None):
        self.value = value
        self.nxt = nxt
        self.prv = prv

    def __repr__(self):
        nxt = None if self.nxt is None else self.nxt.value
        prv = None if self.prv is None else self.prv.value
        return f"<prv:{prv} this:{self.value} nxt:{nxt}>"


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


def get_value_node_dict(node):
    v_n = dict()
    for x in iterate(node):
        if x.value in v_n.keys():
            break
        v_n[x.value] = x
    return v_n


def get_value_set(node):
    a_s = set()
    for x in iterate(node):
        if x is None:
            break
        if x.value in a_s:
            break
        a_s.add(x.value)
    return a_s


def get_value_chain(node):
    a_s = []
    for x in iterate(node):
        if x is None:
            break
        if x.value in a_s:
            break
        a_s.append(x.value)
    return a_s


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
    current = construct_DLL(inp)
    vnd = get_value_node_dict(current)
    for _ in range(100):
        current = move(current, max=max(inp), v_n=vnd)

    return get_value_chain(current)


def p2(inp):
    arrlen = int(1e6)
    numiters = int(1e7)
    a = inp + [i for i in range(10, arrlen + 1)]
    current = construct_DLL(a)

    vnd = get_value_node_dict(current)
    for _ in range(numiters):
        current = move(current, max=arrlen, v_n=vnd)

    return vnd[1].nxt.value * vnd[1].nxt.nxt.value


import time

t0 = time.time()
print(p1(real_input))
print(f"dll {time.time() - t0}")

t0 = time.time()
print(p2(real_input))
print(f"dll {time.time() - t0}")
