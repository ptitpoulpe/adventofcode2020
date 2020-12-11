#!/usr/bin/env python3
import re


def parse(path):
    passports = []
    passport = {}
    with open(path) as f:
        for line in f.read().split("\n"):
            if line == "":
                passports.append(passport)
                passport = {}
            else:
                for kv in line.split(" "):
                    k, v = kv.split(":")
                    passport[k] = v
    return passports


REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} #, "cid"}
def partOne(passports):
    valid_count = 0
    for passport in passports:
        if passport.keys() >= REQUIRED_FIELDS:
            valid_count += 1
    return valid_count


FIELDS_CHECK = {
    "byr": lambda x: 1920 <= int(x) and int(x) <= 2002,
    "iyr": lambda x: 2010 <= int(x) and int(x) <= 2020,
    "eyr": lambda x: 2020 <= int(x) and int(x) <= 2030,
    "hgt": lambda x: False if (m := re.match("^(\d+)(cm|in)$", x)) is None \
                           else 150 <= int(m.group(1)) and int(m.group(1)) <= 193 if m.group(2) == "cm" \
                           else 59 <= int(m.group(1)) and int(m.group(1)) <= 76,
    "hcl": lambda x: re.match("^#[0-9a-f]{6,6}$", x) is not None,
    "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
    "pid": lambda x: re.match("^\d{9,9}$", x) is not None,
    #"cid": lambda x: True,
}
def partTwo(passports):
    valid_count = 0
    for passport in passports:
        valid = True
        if not passport.keys() >= REQUIRED_FIELDS:
            continue
        for key, check in FIELDS_CHECK.items():
            if not check(passport[key]):
                valid = False
                break
        if valid:
            valid_count += 1
    return valid_count


if __name__=="__main__":
    passports = parse("input")

    print("PartOne: {}".format(partOne(passports)))
    print("PartTwo: {}".format(partTwo(passports)))