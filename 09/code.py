#!/usr/bin/env python3
import re
from collections import defaultdict
from functools import lru_cache


def parse(path):
    with open(path) as f:
        return [int(line) for line in f.read().split("\n") if line]


def partOne(numbers):
    sums = [
        numbers[i] + numbers[j]
        for i in range(25)
        for j in range(25)
        if i != j
    ]
    for i in range(25, len(numbers)):
        x = numbers[i]
        if x not in sums:
            return x
        sums = sums[24:] + [x + y for y in numbers[i-24:i]]


def partTwo(numbers):
    number = partOne(numbers)
    start = 0
    stop = 0
    s = 0
    while True:
        if s == number:
            r = numbers[start:stop]
            return min(r) + max(r)
        elif s < number:
            s += numbers[stop]
            stop += 1
        elif s > number:
            s -= numbers[start]
            start += 1

if __name__=="__main__":
    numbers = parse("input")

    print("PartOne: {}".format(partOne(numbers)))
    print("PartTwo: {}".format(partTwo(numbers)))