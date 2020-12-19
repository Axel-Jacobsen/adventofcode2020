#! /usr/bin/env python3


def get_rule_dict(rules):
    """
    k: [[opt1], [opt2], ...] where union of opts is the string
    """
    rule_dict = dict()
    for rule in rules.split("\n"):
        k, v = rule.split(": ")
        if '"' in v:
            rule_rules = [[v.replace('"', "")]]
        else:
            rule_rules = [[int(t) for t in s.strip().split(" ")] for s in v.split("|")]
        rule_dict[int(k)] = rule_rules
    return rule_dict


def evaluate(rule_dict, k):
    """Return list of strings that are valid according to rule k"""
    subv = rule_dict[k]
    options = []
    for opt in subv:
        strs = [""]
        for val in opt:
            if isinstance(val, str):
                # add val to the end of every str in strs
                i = 0
                while i < len(strs):
                    strs[i] += val
                    i += 1
            elif isinstance(val, int):
                # val is an int - get a list of strings
                new_strs = []
                i = 0
                for s in strs:
                    for val_opt in evaluate(rule_dict, val):
                        new_strs.append(s + val_opt)
                    i += 1
                strs = new_strs
        options.extend(strs)

    return options


def eval_msg(msg, rule_dict):
    """
    Need to construct "match options" from rule_dict, and compare those to the msg.
    Rule 0 is the cardinal rule.
    """
    print()


def p1(fname):
    with open(fname, "r") as f:
        rules_str, msgs_str = f.read().split("\n\n")

    rd = get_rule_dict(rules_str)
    rules = evaluate(rd, 0)

    msgs = msgs_str.strip().split("\n")

    s = 0
    for msg in msgs:
        s += int(msg in rules)
    return s


def p2(fname):
    contents = proc_f(fname)


print(p1("input.txt"))
