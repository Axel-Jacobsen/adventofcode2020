#! /usr/bin/env python3


def p1():
    with open("input.txt", "r") as f:
        # all rated can also take 1 to 3 J below their output
        adapter_output_joltage_ratings = sorted(
            [int(i) for i in f.read().split("\n") if i != ""]
        )

        j1_diff = 0
        j2_diff = 0
        j3_diff = 1  # internal joltage

        curr_joltage = 0
        while adapter_output_joltage_ratings != []:
            lowest = adapter_output_joltage_ratings.pop(0)
            diff = lowest - curr_joltage
            j1_diff += int(diff == 1)
            j2_diff += int(diff == 2)
            j3_diff += int(diff == 3)
            curr_joltage = lowest

        return j1_diff * j3_diff


def get_io_pairs(fname="test_input.txt"):
    # return joltage ratings with only "free choices" for adapters
    with open(fname, "r") as f:
        # all rated can also take 1 to 3 J below their output
        joltage_ratings = sorted(
            [[int(i), int(i)] for i in f.read().split("\n") if i != ""]  # (i,o)
        )
        del_idxs = []
        for i in range(1, len(joltage_ratings)):
            if joltage_ratings[i][0] - joltage_ratings[i - 1][1] == 3:
                # all permutations require these two numbers
                joltage_ratings[i][0] = joltage_ratings[i - 1][1]
                del_idxs.append(i - 1)

        for idx in del_idxs[::-1]:
            del joltage_ratings[idx]

        return joltage_ratings


def get_jolts(fname="test_input.txt"):
    with open(fname, "r") as f:
        return sorted([int(v.strip()) for v in f.read().split("\n") if v != ""])


def get_next_valid_cjs(prev, condensed_joltages):
    """get all condensed joltage pairs that would validly
    adapt with out. O(n), it will only take the first
    1, 2, or 3 pairs
    """
    nexts = []
    for cj in condensed_joltages:
        if cj[0] <= prev + 3:
            nexts.append(cj)
        else:
            break
    assert len(nexts) <= 3, f"nexts are {nexts} for {prev}"
    return nexts


def get_next_valids(prev, joltages):
    """get all condensed joltage pairs that would validly
    adapt with out. O(n), it will only take the first
    1, 2, or 3 pairs
    """
    nexts = []
    for j in joltages:
        if j <= prev + 3:
            nexts.append(j)
        else:
            break

    assert len(nexts) <= 3, f"nexts are {nexts} for {prev}"
    return nexts


def p2():
    num_valids = 0
    joltages = get_jolts()
    valids_map = {v: get_next_valids(v, joltages[i+1:]) for i, v in enumerate(joltages)}
    print(valids_map)
    # for i in range(1, len(condensed_joltages)):
    #     previous, nextious = condensed_joltages[i-1]
    #     print(previous, nextious, get_next_valids(nextious, condensed_joltages[i:]))


print(p1())
print(p2())
