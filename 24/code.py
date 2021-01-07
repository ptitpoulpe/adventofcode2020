#!/usr/bin/env python3
from collections import defaultdict

# https://www.redblobgames.com/grids/hexagons/#coordinates
directions = {
    "ne": ( 0,  1, -1),
    "e" : (-1,  1,  0),
    "se": (-1,  0,  1),
    "nw": ( 1,  0, -1),
    "w" : ( 1, -1,  0),
    "sw": ( 0, -1,  1),
}
def parse(path):
    with open(path) as f:
        for line in f.read().split("\n"):
            if not line:
                continue
            hex_path = []
            while line:
                for direction, coordinates in directions.items():
                    if line.startswith(direction):
                        hex_path.append((direction, coordinates))
                        line = line[len(direction):]
            yield hex_path


def flipHex(hex_pathes):
    flip = defaultdict(int)
    for hex_path in hex_pathes:
        x, y, z = 0, 0, 0
        for direction, (sx, sy, sz) in hex_path:
            x += sx
            y += sy
            z += sz
        flip[(x,y,z)] += 1
    return flip


def aroundHex(xyz):
    x, y, z = xyz
    for sx, sy, sz in directions.values():
        yield (x + sx, y + sy, z + sz)


def activate(actives, around):
    new_actives = set()
    known_universe = actives | {
        sxyz
        for xyz in actives
        for sxyz in around(xyz)
    }
    for xyz in known_universe:
        if xyz in actives: # active
            count = 0
            for sxyz in around(xyz):
                if sxyz in actives:
                    count += 1
                if count > 2:
                    break
            if 0 < count and count <= 2:
                new_actives.add(xyz)
        else: # inactive 
            count = 0
            for sxyz in around(xyz):
                if sxyz in actives:
                    count += 1
                if count > 2:
                    break
            if count == 2:
                new_actives.add(xyz)
    return new_actives


def partOne(hex_pathes):
    flip = flipHex(hex_pathes)
    return len([None for count in flip.values() if count % 2 == 1])


def partTwo(hex_pathes):
    flip = flipHex(hex_pathes)
    black = {coordinate for coordinate, count in flip.items() if count % 2 == 1}
    for _ in range(100):
        black = activate(black, aroundHex)
    return len(black)


if __name__=="__main__":
    hex_pathes = list(parse("input"))

    print("PartOne: {}".format(partOne(hex_pathes)))
    print("PartTwo: {}".format(partTwo(hex_pathes)))
