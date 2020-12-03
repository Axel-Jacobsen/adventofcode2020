#! /usr/bin/env python3

def f():
    with open("input.txt", "r") as f:
        nums = [int(i) for i in f.read().split('\n') if i != '']
        for j in range(len(nums)):
            for k in range(len(nums)):
                for l in range(len(nums)):
                    # haha yes n^3 power
                    if nums[j] + nums[k] + nums[l] == 2020:
                        return nums[j] * nums[k] * nums[l]
print(f())
