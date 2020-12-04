#! /usr/bin/env python3

import re


def valid_byr(v):
    return 1920 <= int(v) <= 2002


def valid_iyr(v):
    return 2010 <= int(v) <= 2020


def valid_eyr(v):
    return 2020 <= int(v) <= 2030


def valid_hgt(v):
    v_parsed = re.match(r"(\d+(?:cm|in))", v)
    if v_parsed is None:
        return False

    mtch = v_parsed.group()
    if "cm" in mtch:
        return 150 <= int(mtch.replace("cm", "")) <= 193
    if "in" in mtch:
        return 59 <= int(mtch.replace("in", "")) <= 76


def valid_hcl(v):
    return re.match(r"#[0-9a-f]{6}", v) is not None


def valid_ecl(v):
    ecls = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    for e in ecls:
        if e == v:
            return True
    return False


def valid_pid(v):
    return re.match(r"^\d{9}$", v) is not None


def is_valid(pport):
    necessary = {
        "byr": valid_byr,
        "iyr": valid_iyr,
        "eyr": valid_eyr,
        "hgt": valid_hgt,
        "hcl": valid_hcl,
        "ecl": valid_ecl,
        "pid": valid_pid,
    }
    not_necessary = ["cid"]

    cleaned = re.findall(r"(\w+:[#\w\d]+)", pport)
    passport_kv = {key: val for key, val in [c.split(":") for c in cleaned]}

    for n in necessary.keys():
        if n not in passport_kv.keys():
            return False

        is_valid = necessary[n](passport_kv[n])

        if not is_valid:
            return False
    return True


with open("input.txt", "r") as f:
    ps = f.read().split("\n\n")
    nvalid = 0
    for p in ps:
        nvalid += int(is_valid(p))
    print(nvalid)
