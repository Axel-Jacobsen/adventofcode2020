#! /usr/bin/env python3


from collections import defaultdict


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


def evaluate(rule_dict):
    """Return list of strings that are valid according to rule k"""
    RULE_CACHE = dict()
    loop_keys = set([0])
    loop_cnts = defaultdict(int)

    def _evaluate(rule_dict, k):
        if k in RULE_CACHE.keys():
            return RULE_CACHE[k]

        subv = rule_dict[k]
        options = []
        for opt in subv:

            if k in opt and skip_loops:
                loop_keys.add(k)
                continue

            strs = [""]
            for val in opt:
                if isinstance(val, str):
                    # add val to the end of every str in strs
                    i = 0
                    while i < len(strs):
                        strs[i] += val
                        i += 1
                elif isinstance(val, int):
                    if val == k:
                        if loop_cnts[k] == 4:
                            break
                        else:
                            loop_cnts[k] += 1

                    new_strs = []
                    for s in strs:
                        for val_opt in _evaluate(rule_dict, val):
                            new_strs.append(s + val_opt)

                    strs = new_strs

            options.extend(strs)

        if k not in loop_keys:
            RULE_CACHE[k] = options

        return options

    r0 = _evaluate(rule_dict, 0)

    return r0, loop_keys, RULE_CACHE


def evaluate_loops(msgs, loop_keys, RULE_CACHE):
    for msg in msgs:
        subv = rule_dict[0]
        options = []
        for opt in subv:
            if k in opt and skip_loops:
                loop_keys.add(k)
                continue

            strs = [""]
            for val in opt:


def p1(fname):
    import time

    with open(fname, "r") as f:
        rules_str, msgs_str = f.read().split("\n\n")

    rd = get_rule_dict(rules_str)
    msgs = msgs_str.strip().split("\n")

    t0 = time.time()
    r0, loop_keys, RULE_CACHE = evaluate(rd)
    rules = set(r0)
    print(time.time() - t0)

    s = 0
    for msg in msgs:
        s += int(msg in rules)
    return s


def p2(fname):
    contents = proc_f(fname)


print(p1("test_input_4.txt"))
