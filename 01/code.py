#!/usr/bin/env python3


def parse():
    with open("input") as f:
        return {int(l) for l in f.readlines()}  


def partOne(values):
    return set(v*c for v in values if (c := 2020 - v) in values)


def partTwo(values):
    res = [(0, 1)]
    for i in range(3):
        res = [
            (sv, m * v)
            for s, m in res
            for v in values
            if (sv := s + v) <= 2020
        ]
    return set(m for s, m in res if s == 2020)


if __name__=="__main__":
    values = parse()
    print("Part One: {}".format(partOne(values)))
    print("Part Two: {}".format(partTwo(values)))
