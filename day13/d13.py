#! /usr/bin/env python3


def closest_over(target, period):
    """
    return the smallest number greater than target
    that is divisible by period

    """
    for i in range(target, target + period):
        if i % period == 0:
            return i



def p1():
    with open("input.txt", "r") as f:
        earliest_timestamp = int(f.readline().strip())
        busses = [int(b) for b in f.readline().split(",") if b != "x"]
        earliests = sorted([(b, closest_over(earliest_timestamp, b)) for b in busses], key=lambda v: v[1])
    return earliests[0][0] * (earliests[0][1] - earliest_timestamp)


def p2():
    with open("input.txt", "r") as f:
        f.readline()  # first line useless
        busses = [int(b) for b in f.readline().split(",") if b != "x"]

    return 0

print(p1(), p2())
