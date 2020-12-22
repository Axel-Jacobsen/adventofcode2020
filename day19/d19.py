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

            if k in opt:
                loop_keys.add(k)
                continue

            strs = [""]
            for val in opt:
                if isinstance(val, str):
                    i = 0
                    while i < len(strs):
                        strs[i] += val
                        i += 1
                elif isinstance(val, int):
                    if val == k:
                        if loop_cnts[k] == 1:
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


def get_matching_partials(msg, rule_options, rule_dict):
    """give this rd[8] == [[42], [42, 42], ...]
    yield matching substrings of msg starting from end
    of match of rd

    only 1 of the rule strings will start out msg
    """
    for rule_opt in rule_options:
        consumed_len = 0
        prev_rule_int_successful = True

        for rule_int in rule_opt:

            rule_str_len = len(rule_dict[rule_int][0])

            if msg[consumed_len : consumed_len + rule_str_len] in rule_dict[rule_int]:
                consumed_len += rule_str_len
            else:
                prev_rule_int_successful = False
                break

        if prev_rule_int_successful:
            yield msg[:consumed_len], msg[consumed_len:]


def p2(fname):
    import time

    with open(fname, "r") as f:
        rules_str, msgs_str = f.read().split("\n\n")
        rd = get_rule_dict(rules_str)
        msgs = msgs_str.strip().split("\n")

    t0 = time.time()
    _, loop_keys, partial_rd = evaluate(rd)
    print(time.time() - t0)

    rd[8] = [
        [42],
        [42, 42],
        [42, 42, 42],
        [42, 42, 42, 42],
        [42, 42, 42, 42, 42],
        [42, 42, 42, 42, 42, 42],
        [42, 42, 42, 42, 42, 42, 42],
        [42, 42, 42, 42, 42, 42, 42, 42],
        [42, 42, 42, 42, 42, 42, 42, 42, 42],
    ]
    rd[11] = [
        [42, 31],
        [42, 42, 31, 31],
        [42, 42, 42, 31, 31, 31],
        [42, 42, 42, 42, 31, 31, 31, 31],
        [42, 42, 42, 42, 42, 31, 31, 31, 31, 31],
        [42, 42, 42, 42, 42, 42, 31, 31, 31, 31, 31, 31],
    ]

    # So now we have the RULE_CACHE (in var partial_rd), which is a filled out
    # rule_dict with strings instead of the rules, except for rules which contain
    # loops. We now try to lazily evaluate the messages.
    t0 = time.time()
    num_valid = 0
    for msg in msgs:
        fnd = False
        for pre_v, post_v in get_matching_partials(msg, rd[8], partial_rd):
            for pre_w, post_w in get_matching_partials(post_v, rd[11], partial_rd):
                if post_w == "":
                    fnd = True
                    num_valid += 1
                    break
            if fnd:
                break

    print(time.time() - t0)
    return num_valid


print(p1("input_2.txt"))
print(p2("input_2.txt"))
