#!/usr/bin/env python3


class Map:

    def __init__(self, map):
        self.height = map.count("\n")
        self.width = len(map.split("\n", 1)[0])
        self.map = map.replace("\n", "")

    def get(self, x, y):
        x = x % self.width
        return self.map[self.width * y + x]

    def is_tree(self, x, y):
        return self.get(x, y) == "#"

def treeEncountered(slope_x, slope_y):
    x, y = 0, 0
    trees = 0
    try:
        while True:
            x, y = x + slope_x, y + slope_y
            if map.is_tree(x, y):
                trees += 1
    except IndexError:
        return trees  


def partOne(map):
    return treeEncountered(3, 1)


def partTwo(map):
    result = 1
    for slope_x, slope_y in [(1,1), (3,1), (5,1), (7,1), (1,2)]:
        result *= treeEncountered(slope_x, slope_y)
    return result


if __name__=="__main__":
    map = Map(open("input").read())

    print("PartOne: {}".format(partOne(map)))
    print("PartTwo: {}".format(partTwo(map)))