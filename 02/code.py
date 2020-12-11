#!/usr/bin/env python3

import re


LINE_REG = re.compile(r"(\d+)-(\d+) (\w): (\w+)")
def parse():
    with open("input") as f:
        for l in f.readlines():
            i, j, letter, word = LINE_REG.match(l).groups()
            yield int(i), int(j), letter, word


def validOne(min_, max_, letter, word):
    count = 0
    for char in word:
        if char == letter:
            count += 1
            if count > max_:
                return False
    if count < min_:
        return False
    return True


def partOne(values):
    valid_count = 0
    for min_, max_, letter, word in values:
        if validOne(min_, max_, letter, word):
            valid_count += 1
    return valid_count


def validTwo(pos1, pos2, letter, word):
    return  (word[pos1-1] == letter) ^ (word[pos2-1] == letter)


def partTwo(values):
    valid_count = 0
    for pos1, pos2, letter, word in values:
        if validTwo(pos1, pos2, letter, word):
            valid_count += 1
    return valid_count


if __name__=="__main__":
    values = list(parse())
    print("PartOne: {}".format(partOne(values)))
    print("PartTwo: {}".format(partTwo(values)))
