#!/usr/bin/env python3
from enum import Enum


class Direction(Enum):
    NORTH = (0, 1)
    NORTH_EAST = (1, 1)
    EAST = (1, 0)
    SOUTH_EAST = (1, -1)
    SOUTH = (0, -1)
    SOUTH_WEST = (-1, -1)
    WEST = (-1, 0)
    NORTH_WEST = (-1, 1)


class Map:
    def __init__(self, map):
        self.map = map
        self.height = len(self.map)
        self.width = len(self.map[0])

    @classmethod
    def parse(cls, path):
        with open(path) as f:
            return Map([
                [pos for pos in line]
                for line in f.read().split("\n")
                if line])
        
    def coordinates(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y)

    def get(self, x, y):
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            return self.map[y][x]

    def set(self, x, y, value):
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            self.map[y][x] = value

    def around(self, x, y):
        for d in Direction:
            sx, sy = d.value
            nx, ny = sx + x, sy + y
            v = self.get(nx, ny)
            if v is not None:
                yield v

    def around_sight(self, x, y):
        for d in Direction:
            sx, sy = d.value
            nx, ny = x, y
            while True:
                nx, ny = sx + nx, sy + ny
                v = self.get(nx, ny)
                if v is None:
                    break
                if v in "#L":
                    yield v
                    break
                    
    def round(self, new_state):
        new_map = Map([
            [pos for pos in line]
            for line in self.map
        ])
        for x, y in self.coordinates():
            new_map.set(x, y, new_state(x, y))
        return new_map
    
    def new_state_one(self, x, y):
        if self.get(x, y) == "L":
            for v in self.around(x, y):
                if v == "#":
                    return "L"
            return "#"
        elif self.map[y][x] == "#":
            count = 0
            for v in self.around(x, y):
                if v == "#":
                    count += 1
                if count == 4:
                    return "L"
            return "#"
        else:
            return "." 

    def new_state_two(self, x, y):
        if self.get(x, y) == "L":
            for v in self.around_sight(x, y):
                if v == "#":
                    return "L"
            return "#"
        elif self.map[y][x] == "#":
            count = 0
            for v in self.around_sight(x, y):
                if v == "#":
                    count += 1
                if count == 5:
                    return "L"
            return "#"
        else:
            return "." 

    def equal(self, othermap):
        for x, y in self.coordinates():
            if self.map[y][x] != othermap.map[y][x]:
                return False
        return True

    def occupied(self):
        count = 0
        for x, y in self.coordinates():
            if self.map[y][x] == "#":
                count += 1
        return count

    def print(self):
        for line in self.map:
            print("|{}|".format("".join(line)))
        print()

def partOne(map):
    while True:
        new_map = map.round(map.new_state_one)
        if map.equal(new_map):
            return new_map.occupied()
        else:
            map = new_map

def partTwo(map):
    while True:
        new_map = map.round(map.new_state_two)
        if map.equal(new_map):
            return new_map.occupied()
        else:
            map = new_map

if __name__=="__main__":
    map = Map.parse("input")

    print("PartOne: {}".format(partOne(map)))
    print("PartTwo: {}".format(partTwo(map)))