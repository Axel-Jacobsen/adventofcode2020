#! /usr/bin/env python3


def closest_over(target, period):
    """
    return the smallest number greater than target
    that is divisible by period

    """
    for i in range(target, target + period):
        if i % period == 0:
            return i


def p1(fname):
    with open(fname, "r") as f:
        earliest_timestamp = int(f.readline().strip())
        busses = [int(b) for b in f.readline().split(",") if b != "x"]
        earliests = sorted(
            [(b, closest_over(earliest_timestamp, b)) for b in busses],
            key=lambda v: v[1],
        )
    return earliests[0][0] * (earliests[0][1] - earliest_timestamp)


"""
For part two, we have a set of equations given by the bus string.
We can solve this via the Chinese Remainder Theorem.

(t | 7) ^ (t + 1 | 13) ^ (t + 4 | 59) ^ ...


7a = t
13b - 1 = t
59c - 4 = t
31d - 6 = t
19g - 7 = t

equiv. to

t = -0 (mod 7)
t = -1 (mod 13)
t = -4 (mod 59)
t = -6 (mod 31)
t = -7 (mod 19)

given two congruences (such as the first two equations)

x = a1 (mod n1)
x = a2 (mod n2)

a solution can be given by

x = a1m2n2 + a2m1n1, where

m1n1 + m2n2 = 1 and Extended Euclidian Algorithm gives m1 and m2


for

x = 0 (mod 3)  [1]
x = 3 (mod 4)  [2]
x = 4 (mod 5)  [3]

First, apply Bezout's identity for 3 and 4
(i.e. get 1 and -1 as the bezout coefficients)

(1) * 4 + (-1) * 3 = 1

Put this into the formula for x = a1m2n2 + a2m1n1 to get

x = 0 * 1 * 4 + 3 * (-1) * 3 = -9

This is a solution to [1] and [2]. Other solutions are obtained
from adding x (i.e. -9) to n1*n2 (i.e. 3 * 4 = 12), so (-9 + 12 = 3)

Next get bezout's coefficients for 5 and n1*n2=3*4=12 to get (5, -2)

Put this into the formula for x = a1m2n2 + a2m1n1 to get

x = 5 * 5 * 3 - 24 * 4 = -21

repeat this for all congruences, and add a multiple of ni to get the
first positive number
"""


def p2(fname, fnc):
    with open(fname, "r") as f:
        f.readline()  # first line useless
        return fnc(format_bus_str(f.readline()))


def format_bus_str(bus_str, neg_idx=False):
    return sorted(
        [(i, int(b)) for i, b in enumerate(bus_str.strip().split(",")) if b != "x"],
        key=lambda v: v[1],
        reverse=True,
    )


def get_earliest_timestamp_brute(busses):
    lb_offset, lb = busses[0]
    t = lb
    while True:
        valid = True
        for t_offset, bus_num in busses[1:]:
            if (t + t_offset - lb_offset) % bus_num != 0:
                valid = False
                break

        if valid:
            return t - lb_offset

        t += lb


def bezout_coeff(a, b):
    """Thanks, Wikipedia!

    For a * m1 + b * m2 = 1, return (m1, m2)
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    return old_s, old_t


def p2_mod_chinese_remainder_thm(busses):
    """
    busses is a list of k pairs [-a1,n1] for x = a1 (mod n1)
    for a1..ak and n1..nk

    e.g. we want
    >>> p2_mod_chinese_remainder_thm([
            (0,3),
            (3,4),
            (4,5),
        ])
    21

    for schedule "3,x,x,4,5"
    """
    # Our system of equations comes out to
    # the indexes being negative for CRT
    busses = [(-i, b) for i, b in busses]

    ai, ni = busses[0]
    for ac, nc in busses[1:]:
        mi, mc = bezout_coeff(ni, nc)
        ai = ai * nc * mc + ac * ni * mi
        ni = ni * nc

    return ai + ni * (abs(ai) // ni + 1)


def test_p2(p2_fnc):
    assert (
        p2_fnc(format_bus_str("67,7,59,61")) == 754018
    ), f'{p2_fnc(format_bus_str("67,7,59,61"))}, 754018'
    assert (
        p2_fnc(format_bus_str("67,x,7,59,61")) == 779210
    ), f'{p2_fnc(format_bus_str("67,x,7,59,61"))} 779210'
    assert (
        p2_fnc(format_bus_str("67,7,x,59,61")) == 1261476
    ), f'{p2_fnc(format_bus_str("67,7,x,59,61"))}, 1261476'
    assert (
        p2_fnc(format_bus_str("1789,37,47,1889")) == 1202161486
    ), f'{p2_fnc(format_bus_str("1789,37,47,1889"))}, 1202161486'


if __name__ == "__main__":
    print(p1(fname="input.txt"))
    test_p2(get_earliest_timestamp_brute)
    test_p2(p2_mod_chinese_remainder_thm)
    print(p2("input.txt", p2_mod_chinese_remainder_thm))
