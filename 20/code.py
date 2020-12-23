#!/usr/bin/env python3
from collections import defaultdict
from enum import Enum


class Tile:
    """
    For tile:
        123
        456
        789
    Top: 123
    Bottom: 987
    Left: 741
    Right: 369
    """

    def __init__(self, name, values):
        self.name = name
        self.values = values
        top = values[0]
        bottom = list(reversed(values[-1]))
        left = list(reversed([value[0] for value in values]))
        right = [value[-1] for value in values]
        self.ntop = self.to_int(top)
        self.rtop = self.to_int(reversed(top))
        self.nbottom = self.to_int(bottom)
        self.rbottom = self.to_int(reversed(bottom))
        self.nleft = self.to_int(left)
        self.rleft = self.to_int(reversed(left))
        self.nright = self.to_int(right)
        self.rright = self.to_int(reversed(right))
        self.all = {
            self.ntop, self.rtop,
            self.nbottom, self.rbottom,
            self.nleft, self.rleft, 
            self.nright, self.rright
        }
        self.unboundable = []
        self.x = None
        self.y = None

    def to_int(self, array):
        return int("".join("0" if e else "1" for e in array), 2)

    def unbound(self, others):
        self.unboundable = set()
        others = set.union(*(other.all for other in others if other != self))
        for name, normal, reverse in [
            ("top", self.ntop, self.rtop),
            ("bottom", self.nbottom, self.rbottom),
            ("left", self.nleft, self.rleft),
            ("right", self.nright, self.rright)
        ]:
            if normal not in others and reverse not in others:
                self.unboundable.add(name)

    def set_coordinate(self, x, y):
        self.x = x
        self.y = y

    def rotate(self):
        self.values = [list(reversed(line)) for line in zip(*self.values)]
        ntmp = self.ntop
        rtmp = self.rtop
        self.ntop = self.nleft
        self.rtop = self.rleft
        self.nleft = self.nbottom
        self.rleft = self.rbottom
        self.nbottom = self.nright
        self.rbottom = self.rright
        self.nright = ntmp
        self.rright = rtmp
        self.unboundable = {
            "top" if u == "left" else
            "left" if u == "bottom" else
            "bottom" if u == "right" else
            "right"
            for u in self.unboundable
        }

    def flipV(self):
        self.values = [
            list(reversed(line))
            for line in self.values
        ]
        self.nleft, self.rright = self.rright, self.nleft
        self.rleft, self.nright = self.nright, self.rleft
        self.ntop, self.rtop = self.rtop, self.ntop
        self.nbottom, self.rbottom = self.rbottom, self.nbottom
        self.unboundable = {
            "left" if u == "right" else
            "right" if u == "left" else
            u
            for u in self.unboundable
        }

    def flipH(self):
        self.values = list(reversed(self.values))
        self.ntop, self.rbottom = self.rbottom, self.ntop
        self.rtop, self.nbottom = self.nbottom, self.rtop
        self.nleft, self.rleft = self.rleft, self.nleft
        self.nright, self.rright = self.rright, self.nright
        self.unboundable = {
            "top" if u == "bottom" else
            "bottom" if u == "top" else
            u
            for u in self.unboundable
        }

    def getn(self, direction):
        return getattr(self, "n" + direction)
    
    def getr(self, direction):
        return getattr(self, "r" + direction)

    def match(self, value, direction):
        while self.getn(direction) != value and self.getr(direction) != value:
            self.rotate()
        if self.getr(direction) == value:
            if direction in ("top", "bottom"):
                self.flipV()
            else:
                self.flipH()

    def print(self, draw=False):
        print(f"""
Tile {self.name}:
  top: {self.ntop}/{self.rtop}
  left: {self.nleft}/{self.rleft}
  bottom: {self.nbottom}/{self.rbottom}
  right: {self.nright}/{self.rright}
  unboundable: {self.unboundable}
  coord: {self.x}, {self.y}
        """)
        if draw:
            for line in self.values[1:-1]:
                print("    " + "".join("#" if char else "." for char in line[1:-1]))


def parse(path):
    with open(path) as f:
        tiles = []
        for tile_section in f.read().split("\n\n"):
            if tile_section:
                lines = tile_section.split("\n")
                name = int(lines[0][5:-1])
                values = [
                    [char == "#" for char in line]
                    for line in lines[1:]
                    if line
                ]
                tiles.append(Tile(name, values))
        return tiles


def get_dragon_coords(dragon):
    dragon_coords = []
    for x, line in enumerate(dragon):
        for y, char in enumerate(line):
            if char:
                dragon_coords.append((x, y))
    return dragon_coords


def get_dragons_coords():
    dragon_str = (
        "                  # \n"
        "#    ##    ##    ###\n"
        " #  #  #  #  #  #   "
    )
    dragon_top = [
        [char == "#" for char in line]
        for line in dragon_str.split("\n")
    ]
    dragon_left = [list(reversed(line)) for line in zip(*dragon_top)]
    dragon_bottom = [list(reversed(line)) for line in zip(*dragon_left)]
    dragon_right = [list(reversed(line)) for line in zip(*dragon_bottom)]

    dragons = []
    for dragon in [dragon_top, dragon_left, dragon_bottom, dragon_right]:
        dragons.append(dragon)
        dragons.append([list(reversed(line)) for line in dragon])
        dragons.append(list(reversed(dragon)))
    
    return [get_dragon_coords(dragon) for dragon in dragons]

def match_dragon(x, y, puzzle, dragon):
    try:
        for sx, sy in dragon:
            if puzzle[x + sx][y + sy] == ".":
                return False
    except:
        return False
    return True

def show_dragon(x, y, puzzle, dragon):
    for sx, sy in dragon:
        puzzle[x + sx][y + sy] = "O"

def partOne(tiles):
    result = 1
    for tile in tiles:
        tile.unbound(tiles)
        if len(tile.unboundable) == 2:
            result *= tile.name
    return result


def partTwo(tiles):
    corners = []
    all = defaultdict(set)
    for tile in tiles:
        tile.unbound(tiles)
        if len(tile.unboundable) == 2:
            corners.append(tile)

        for side in tile.all:
            all[side].add(tile)

    # Starter
    tile = corners.pop()
    tile.set_coordinate(0, 0)
    for i in tile.all:
        all[i].remove(tile)
    while tile.unboundable != {"top", "left"}:
        tile.rotate()
    
    tiles_todo = [tile]
    done = [tile]
    while len(tiles_todo) and (tile_todo := tiles_todo.pop(0)):
        # Right
        right = all[tile_todo.nright]
        if len(right) == 1:
            right = list(right)[0]
            right.match(tile_todo.rright, "left")
            assert right.rleft == tile_todo.nright
            for i in right.all:
                all[i].remove(right)
            right.unboundable.add("left")
            right.set_coordinate(tile_todo.x, tile_todo.y + 1)
            done.append(right)
            tiles_todo.append(right)

        # Bottom
        bottom = all[tile_todo.nbottom]
        if len(bottom) == 1:
            bottom = list(bottom)[0]
            bottom.match(tile_todo.rbottom, "top")
            assert bottom.rtop == tile_todo.nbottom
            for i in bottom.all:
                all[i].remove(bottom)
            bottom.unboundable.add("top")
            bottom.set_coordinate(tile_todo.x + 1, tile_todo.y)
            done.append(bottom)
            if "bottom" not in bottom.unboundable:
                tiles_todo.append(bottom)
    
    puzzle_tiles = { (tile.x, tile.y): tile for tile in done }

    max_x = max([tile.x for tile in done])
    max_y = max([tile.y for tile in done])

    puzzle = [
        [None for _ in range(8 * (max_x + 1))]
        for _ in range(8 * (max_y + 1))
    ]
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            tile = puzzle_tiles[(x, y)]
            for sx in range(8):
                for sy in range(8):
                    puzzle[x * 8 + sx][y * 8 + sy] = "#" if tile.values[1 + sx][1 + sy] else "."

    dragons = get_dragons_coords()
    for x in range(len(puzzle)):
        for y in range(len(puzzle[0])):
            for dragon in dragons:
                if match_dragon(x, y, puzzle, dragon):
                    show_dragon(x, y, puzzle, dragon)

    return "\n".join("".join(line) for line in puzzle).count("#")
    

if __name__=="__main__":
    tiles = parse("input")

    print("PartOne: {}".format(partOne(tiles)))
    print("PartTwo: {}".format(partTwo(tiles)))
