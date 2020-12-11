#!/usr/bin/env python3


def parse(path):
    with open(path) as f:
        for line in f.read().split("\n"):
            if not line:
                continue
            row = int(line[:7].replace("F", "0").replace("B", "1"), base=2)
            column = int(line[7:].replace("L", "0").replace("R", "1"), base=2)
            seat = row * 8 + column
            yield row, column, seat       


def partOne(tickets):
    return max(seat for _, _, seat in tickets)

def partTwo(tickets):
    seats = {seat for _, _, seat in tickets}
    return set(range(min(seats), max(seats))) - seats

if __name__=="__main__":
    tickets = list(parse("input"))

    print("PartOne: {}".format(partOne(tickets)))
    print("PartTwo: {}".format(partTwo(tickets)))