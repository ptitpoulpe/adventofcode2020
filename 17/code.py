#!/usr/bin/env python3


def parse(path):
    with open(path) as f:
        actives = set()
        for x, line in enumerate(f.read().split("\n")):
            for y, char in enumerate(line):
                if char == "#":
                    actives.add((x, y, 0))
        return actives


shifts3d = [
    (x, y, z)
    for x in (-1, 0, 1)
    for y in (-1, 0, 1)
    for z in (-1, 0, 1)
    if not( x == 0 and y == 0 and z == 0)
]
def around3d(xyz):
    x, y, z = xyz
    for sx, sy, sz in shifts3d:
        yield (x + sx, y + sy, z + sz)


shifts4d = [
    (x, y, z, w)
    for x in (-1, 0, 1)
    for y in (-1, 0, 1)
    for z in (-1, 0, 1)
    for w in (-1, 0, 1)
    if not( x == 0 and y == 0 and z == 0 and w == 0)
]
def around4d(xyzw):
    x, y, z, w = xyzw
    for sx, sy, sz, sw in shifts4d:
        yield (x + sx, y + sy, z + sz, w + sw)


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
                if count > 3:
                    break
            if count == 2 or count == 3:
                new_actives.add(xyz)
        else: # inactive 
            count = 0
            for sxyz in around(xyz):
                if sxyz in actives:
                    count += 1
                if count > 3:
                    break
            if count == 3:
                new_actives.add(xyz)
    return new_actives


def partOne(actives):
    for i in range(6):
        actives = activate(actives, around3d)
    return len(actives)


def partTwo(actives):
    actives = {(x,y,z,0) for x, y, z in actives}
    for i in range(6):
        actives = activate(actives, around4d)
    return len(actives)

if __name__=="__main__":
    actives = parse("input")

    print("PartOne: {}".format(partOne(actives)))
    print("PartTwo: {}".format(partTwo(actives)))