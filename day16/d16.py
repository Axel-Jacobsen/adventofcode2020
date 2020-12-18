#! /usr/bin/env python3


def process_field_strings(field_strings):
    proc_fs = []

    def _proc_rgs_pair(rgs_pair):
        return [
            [int(rg) for rg in rgs_str.split("-")] for rgs_str in rgs_pair.split(" or ")
        ]

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
        field_strings = lines[: lines.index("your ticket:")]
        my_ticket = lines[lines.index("your ticket:") + 1]
        nearby_ticket = lines[lines.index("nearby tickets:") + 1 :]

        return (
            process_field_strings(field_strings),
            process_tickets([my_ticket])[0],
            process_tickets(nearby_ticket),
        )


def is_valid(ticket, fields) -> bool:
    ticket_is_valid = False
    for num in ticket:
        valid = False
        for _, (fb1, fb2) in fields:
            if fb1[0] <= num <= fb1[1] or fb2[0] <= num <= fb2[1]:
                valid = True
                break
        if not valid:
            return False
    return True


def p1(fname):
    fields, my_ticket, nearby_tickets = process_input(fname)
    invalid_vals = []
    for ticket in nearby_tickets:
        for num in ticket:
            valid = False
            for _, (fb1, fb2) in fields:
                if fb1[0] <= num <= fb1[1] or fb2[0] <= num <= fb2[1]:
                    valid = True
                    break
            if not valid:
                invalid_vals.append(num)
    return sum(invalid_vals)


def get_possible_fields(valid_tickets, fields):
    field_possibilities = []
    for ticket in valid_tickets:
        ticket_possibles = []
        for num in ticket:
            ticket_idx = []
            for field, (fb1, fb2) in fields:
                if fb1[0] <= num <= fb1[1] or fb2[0] <= num <= fb2[1]:
                    ticket_idx.append(field)
            ticket_possibles.append(ticket_idx)
        yield ticket_possibles


def get_field_names_for_idxs(fields, my_ticket, valid_tickets):
    # filtered_fields is a list of sets, where the set (after this block) holds
    # only fields that are in every ticket
    all_fields = [f[0] for f in fields]
    filtered_fields = [set(all_fields)] * len(my_ticket)
    for t in get_possible_fields(valid_tickets, fields):
        for i, idx in enumerate(t):
            filtered_fields[i] = filtered_fields[i].intersection(set(idx))

    # repeatedly pass over filtered fields, removing non-unique fields
    fixed_fields = set()
    while not all([len(ff) == 1 for ff in filtered_fields]):
        for field in filtered_fields:
            if len(field) == 1:
                fixed_fields.add(next(iter(field)))
            else:
                field -= fixed_fields

    # each set has 1 element, pop and return final ans
    return [e.pop() for e in filtered_fields]


def p2(fname):
    fields, my_ticket, nearby_tickets = process_input(fname)
    all_fields = [f[0] for f in fields]
    valid_tickets = [ticket for ticket in nearby_tickets if is_valid(ticket, fields)]

    prod = 1
    field_names = get_field_names_for_idxs(fields, my_ticket, valid_tickets)
    for i, fn in enumerate(field_names):
        if "departure" in fn:
            prod *= my_ticket[i]
    return prod


print(p1("input.txt"))
print(p2("input.txt"))
