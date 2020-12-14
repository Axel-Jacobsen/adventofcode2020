#! /usr/bin/env python3


def mask_int(v, mask):
    bin_v = "{:b}".format(v)
    padded_bin_v = list("0" * (36 - len(bin_v)) + bin_v)
    for i, mask_char in enumerate(mask):
        if mask_char != "X":
            padded_bin_v[i] = mask_char
    return int("".join(padded_bin_v), base=2)


def mask_mem_addr(v, mask):
    bin_v = "{:b}".format(v)
    padded_bin_v = list("0" * (36 - len(bin_v)) + bin_v)
    for i, mask_char in enumerate(mask):
        if mask_char == "1":
            padded_bin_v[i] = "1"
        elif mask_char == "X":
            padded_bin_v[i] = "X"
    return padded_bin_v


def get_all_floating_addrs(v):
    mag = v.count("X")
    fas = []
    for i in range(2 ** mag):
        curr_float_addr = v[:]
        bin_i = "{:b}".format(i)
        padded_bin_i = list("0" * (mag - len(bin_i)) + bin_i)
        for b in padded_bin_i:
            curr_float_addr[curr_float_addr.index("X")] = b
        fas.append(int("".join(curr_float_addr), base=2))
    return fas


def p1():
    with open("input.txt", "r") as f:
        MASK = ""
        mem  = dict()
        for line in f:
            s,v = line.strip().split(" = ")
            if s == "mask":
                MASK = v
            else:
                mem_address = int(s.replace("mem[", "").replace("]", ""))
                mem[mem_address] = mask_int(int(v), MASK)
    return sum(mem.values())


def p2():
    with open("input.txt", "r") as f:
        MASK = ""
        mem  = dict()
        for line in f:
            s,v = line.strip().split(" = ")
            if s == "mask":
                MASK = v
            else:
                mem_address = int(s.replace("mem[", "").replace("]", ""))
                mma = mask_mem_addr(mem_address, MASK)
                float_addrs = get_all_floating_addrs(mma)
                for m in float_addrs:
                    mem[m] = int(v)
    return sum(mem.values())


print(p1())
print(p2())
