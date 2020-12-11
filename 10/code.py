#!/usr/bin/env python3
import re
from collections import defaultdict
from functools import lru_cache


def parse(path):
    with open(path) as f:
        return [int(line) for line in f.read().split("\n") if line]


def partOne(numbers):
    s = [0] + sorted(numbers)
    res = defaultdict(int)
    for i, j in zip(s, s[1:]):
        res[j-i] += 1
    res[3] += 1
    return res[1] * res[3]


def partTwo(numbers):
    s = [0] + sorted(numbers)
    res = [0 for _ in s]
    res[-1] = 1
    for i in range(len(s), -1, -1):
        for j in range(i+1, i+4):
            if j >= len(s) or s[j] - s[i] > 3:
                break
            res[i] += res[j]
    return res[0]

if __name__=="__main__":
    numbers = parse("input")

    print("PartOne: {}".format(partOne(numbers)))
    print("PartTwo: {}".format(partTwo(numbers)))