#!/usr/bin/env python3


def parse(path):
    with open(path) as f:
        return [int(i) for i in f.read().split(",")]


def compute(numbers, th):
    last = {}
    i = 1
    # read the list
    for number in numbers[:-1]:
        last[number] = i
        i += 1
    last_spoken = numbers[-1]

    while i < th:
        if last_spoken in last:
            spoken = i - last[last_spoken]
            last[last_spoken] = i
        else:
            spoken = 0
            last[last_spoken] = i
        last_spoken = spoken
        i += 1
    return last_spoken


def partOne(numbers):
    return compute(numbers, 2020)


def partTwo(numbers):
    return compute(numbers, 30000000)


if __name__=="__main__":
    numbers = parse("input")

    print("PartOne: {}".format(partOne(numbers)))
    print("PartTwo: {}".format(partTwo(numbers)))