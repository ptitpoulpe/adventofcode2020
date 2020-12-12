#!/usr/bin/env python3


def parse(path):
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                yield line[0], int(line[1:])


def partOne(instructions):
    x, y = 0, 0
    sx, sy = 1, 0
    for action, value in instructions:
        if action == "N":
            y += value
        elif action == "S":
            y -= value
        elif action == "E":
            x += value
        elif action == "W":
            x -= value
        elif action == "F":
            x += sx * value
            y += sy * value
        elif action == "R":
            while value > 0:
                sx, sy = sy, -sx
                value -= 90
        elif action == "L":
            while value > 0:
                sx, sy = -sy, sx
                value -= 90
    return abs(x) + abs(y)


def partTwo(instructions):
    x, y = 0, 0
    sx, sy = 10, 1
    for action, value in instructions:
        if action == "N":
            sy += value
        elif action == "S":
            sy -= value
        elif action == "E":
            sx += value
        elif action == "W":
            sx -= value
        elif action == "F":
            x += sx * value
            y += sy * value
        elif action == "R":
            while value > 0:
                sx, sy = sy, -sx
                value -= 90
        elif action == "L":
            while value > 0:
                sx, sy = -sy, sx
                value -= 90
    return abs(x) + abs(y)


if __name__=="__main__":
    instructions = list(parse("input"))

    print("PartOne: {}".format(partOne(instructions)))
    print("PartTwo: {}".format(partTwo(instructions)))