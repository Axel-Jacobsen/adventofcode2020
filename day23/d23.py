#! /usr/bin/env python3

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


def _get(arr, idx):
    try:
        return arr.index(idx)
    except ValueError:
        return None


def move(cups, current):
    c = cups[:]
    idx = cups.index(current)

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
        if destination < min(c):
            destination = max(c)
        else:
            destination -= 1

    new = c[: destination_idx + 1] + rem + c[destination_idx + 1 :]
    next_val = (
        new[new.index(current) + 1] if new.index(current) != len(new) - 1 else new[0]
    )

    return new, next_val


def p1(inp):
    a, idx = inp, inp[0]
    for _ in range(100):
        a, idx = move(a, idx)
    return a


print(p1(real_input))
