#!/usr/bin/env python3


def parse(path):
    group = []
    groups = [group]
    with open(path) as f:
        return [
            [
                set(person)
                for person in group.split("\n")
                if person != ""
            ]
            for group in f.read().split("\n\n")
        ]   


def partOne(groups):
    return sum(len(set.union(*group)) for group in groups)


def partTwo(groups):
    return sum(len(set.intersection(*group)) for group in groups)


if __name__=="__main__":
    groups = parse("input")

    print("PartOne: {}".format(partOne(groups)))
    print("PartTwo: {}".format(partTwo(groups)))