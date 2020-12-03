#! /usr/bin/env python3


with open('input.txt', 'r') as f:
    num_valid = 0
    for line in f.readlines():
        policy, pwd = line.split(": ")
        rnge, letter = policy.split(" ")
        rnge = [int(i) for i in rnge.split("-")]
        if rnge[0] <= list(pwd).count(letter) <= rnge[1]:
            num_valid += 1
    print("part 1", num_valid)


with open('input.txt', 'r') as f:
    num_valid = 0
    for line in f.readlines():
        policy, pwd = line.split(": ")
        rnge, letter = policy.split(" ")
        rnge = [int(i) for i in rnge.split("-")]
        if [pwd[rnge[0] - 1], pwd[rnge[1] - 1]].count(letter) == 1:
            num_valid += 1
    print("part 2", num_valid)
