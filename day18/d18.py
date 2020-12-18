#! /usr/bin/env python3


def get_exprs(fname):
    raw_exprs = []
    with open(fname, "r") as f:
        for line in f:
            raw_exprs.append(line.replace(" ", "").strip())
    return raw_exprs


def preprocess(s):
    expr = []
    i = 0
    while i < len(s):
        if s[i] == "(":
            match = i + get_matching_closing(s[i:])
            expr.append(preprocess(s[i + 1 : match]))
            i = match + 1
        elif s[i] == "*":
            expr.append("*")
            i += 1
        elif s[i] == "+":
            expr.append("+")
            i += 1
        else:
            expr.append(int(s[i]))
            i += 1
    return expr


def evaluate(expr):
    cval = 0
    op = "+"
    for v in expr:
        if isinstance(v, list):
            cval = apply(op, cval, evaluate(v))
        elif isinstance(v, str):
            op = v
        elif isinstance(v, int):
            cval = apply(op, cval, v)
    return cval


def get_matching_closing(s):
    """
    s starts with '(', return the index
    of the ')' which matches it
    """
    ctr = 0
    for i in range(len(s)):
        if s[i] == "(":
            ctr += 1
        elif s[i] == ")":
            ctr -= 1
        if ctr == 0:
            return i
    raise RuntimeError(f"no close paren found for {s}")


def apply(op, val1, val2):
    if op == "+":
        return val1 + val2
    if op == "*":
        return val1 * val2
    raise RuntimeError(f"don't know how to handle {op}")


def p1(fname):
    s = 0
    raw_exprs = get_exprs(fname)
    for raw_exp in raw_exprs:
        exp = preprocess(raw_exp)
        s += evaluate(exp)
    return s


print(p1("input.txt"))
