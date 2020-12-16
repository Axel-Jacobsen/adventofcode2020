#! /usr/bin/env python3


def process_field_strings(field_strings):
    proc_fs = []
    def _proc_rgs_pair(rgs_pair):
        return [[int(rg) for rg in rgs_str.split("-")] for rgs_str in rgs_pair.split(" or ")]

    for fs in field_strings:
        field, rgs_pair = fs.split(": ")
        proc_fs.append((field, _proc_rgs_pair(rgs_pair)))
    return proc_fs


def process_tickets(tickets):
    processed = []
    for nbt in tickets:
        processed.append([int(v) for v in nbt.split(",") if v != ""])
    return processed


def process_input(fname):
    with open(fname, "r") as f:
        fields = []
        lines = [l for l in [line.strip() for line in f.read().split("\n")] if l != ""]
        field_strings = lines[:lines.index("your ticket:")]
        my_ticket = lines[lines.index("your ticket:") + 1]
        nearby_ticket = lines[lines.index("nearby tickets:")+1:]

        return (
            process_field_strings(field_strings),
            process_tickets([my_ticket])[0],
            process_tickets(nearby_ticket)
        )

def p1(fname):
    fields, my_ticket, nearby_tickets = process_input(fname)
    invalid_vals = []
    for ticket in nearby_tickets:
        for num in ticket:
            valid = False
            for _, (fb1, fb2) in fields:
                if (fb1[0] <= num <= fb1[1] or fb2[0] <= num <= fb2[1]):
                    valid = True
                    break
            if not valid:
                invalid_vals.append(num)

    return sum(invalid_vals)

print(p1("input.txt"))
