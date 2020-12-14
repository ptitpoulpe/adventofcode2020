#!/usr/bin/env python3
import math


def parse(path):
    with open(path) as f:
        earlier = int(f.readline())
        buses = [
            int(bus) if bus != "x" else None
            for bus in f.readline().split(",")
        ]
        return earlier, buses


def partOne(earlier, buses):
    buses = [bus for bus in buses if bus is not None]
    time = earlier
    while True:
        for bus in buses:
            if time % bus == 0:
                return (time - earlier) * bus
        time += 1


def combine(ab, cd):
    """ a*x + b = c*y + d """
    a, b = ab
    c, d = cd
    gcd = math.gcd(a, b)
    ac = a * c
    while True:
        if b == d:
            return ac, b
        elif b < d:
            b += a * math.ceil((d - b) / a)
        else:
            d += c * math.ceil((b - d) / c)


def partTwo(buses):
    ibuses = [
        [bus, -i]
        for i, bus in enumerate(buses)
        if bus is not None
    ]
    ab = ibuses.pop()
    while len(ibuses):
        cd = ibuses.pop()
        ab = combine(ab, cd)
    return ab[1]


if __name__=="__main__":
    earlier, buses = parse("input")

    print("PartOne: {}".format(partOne(earlier, buses)))
    print("PartTwo: {}".format(partTwo(buses)))