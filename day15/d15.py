#! /usr/bin/env python3

import time


test_starting_nums = [0, 3, 6]
starting_nums = [8,13,1,0,18,9]


def say(nums, max_num):
    if max_num < len(nums):
        raise RuntimeError("NO! NO!")

    last_seen = {}
    for i, n in enumerate(nums[:-1], start=1):
        last_seen[n] = i

    i += 1
    spoken = nums[-1]
    while i < max_num:
        prev_spoken = spoken
        if prev_spoken not in last_seen.keys():
            spoken = 0
        else:
            spoken = i - last_seen[prev_spoken]
        last_seen[prev_spoken] = i
        i += 1

    return spoken


def test_say():
    test_inp_out = [
            ([1,3,2], 1),
            ([2,1,3], 10),
            ([1,2,3], 27),
            ([2,3,1], 78),
            ([3,2,1], 438),
            ([3,1,2], 1836),
        ]

    for inp, out in test_inp_out:
        calc = say(inp, 2020)
        assert calc == out, f"{calc} should be {out} for {inp}"

test_say()
t1 = time.time()
print(say(starting_nums, 2020))
print(say(starting_nums, 30000000))
print(time.time() - t1)
