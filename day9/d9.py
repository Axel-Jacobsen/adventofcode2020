#! /usr/bin/env python3

import time


PREAMBLE_LEN = 25

"""
for any number n at index i (i > 24),
n = inp[a] + inp[b] for some a,b in [i-PREAMBLE_LEN, i - 1]
a != b
a and b are not unique

find the first number which does not have this property
"""
def part1():
    with open("input.txt", "r") as f:
        inp = [int(v) for v in f.read().split("\n") if v != ""]
        for i in range(PREAMBLE_LEN, len(inp)):
            found_sum = False
            for j in range(PREAMBLE_LEN):
                if found_sum: break
                for k in range(j, PREAMBLE_LEN):
                    if inp[i - j - 1] + inp[i - k - 1] == inp[i]:
                        found_sum = True
                        break

            if not found_sum:
                return inp[i]


def part2(target):
    with open("input.txt", "r") as f:
        inp = [int(v) for v in f.read().split("\n") if v != ""]
        for contiguous_sz in range(2, len(inp)):
            for i in range(len(inp) - contiguous_sz):
                if inp[i + contiguous_sz] == target:
                    break
                if sum(inp[i:i+contiguous_sz]) == target:
                    return min(inp[i:i+contiguous_sz]) + max(inp[i:i+contiguous_sz])

target = part1()
print("part1", target)
print("part2", part2(target))
