#!/usr/bin/env python3
import re


def parseOne(path):
    with open(path) as f:
        return [tree(line) for line in f.read().split("\n") if line]

def tree(line):
    tree = []
    lpart = None
    op = None
    for token in re.findall("\d+|[()+-/*]", line):
        if token == "(":
            tree.append((lpart, op))
            lpart = None
            op = None
        elif token == ")":
            _lpart, _op = tree.pop()
            if _op is not None:
                lpart = (_lpart, _op, lpart)
        elif token in "+-*/":
            op = token
        else:
            token = int(token)
            if op is not None:
                lpart = (lpart, op, token)
                op = None
            else:
                lpart = token
    return lpart

def compute(tree):
    if isinstance(tree, tuple):
        lpart, op, rpart = tree
        lpart = compute(lpart)
        rpart = compute(rpart)
        if op == "+":
            return lpart + rpart
        elif op == "*":
            return lpart * rpart
    else:
        return tree

def partOne(trees):
    res = 0
    for tree in trees:
        res += compute(tree)
    return res

def parseTwo(path):
    with open(path) as f:
        return [line for line in f.read().split("\n") if line]

def next(line):
    pos = 0
    max_match = None
    max_score = -1
    while m := re.compile(r"(\d+) ([+*]) (\d+)").search(line, pos):
        open_par = line[:m.start()].count("(")
        close_par = line[:m.start()].count(")")
        bonus = 0.5 if m.group(2) == "+" else 0
        score = open_par - close_par + bonus
        if score > max_score:
            max_match = m
            max_score = score
        pos = m.start(3)
    return max_match

def partTwo(lines):
    # with only regex (only for fun)
    res = 0
    for line in lines:
        while True:
            if re.fullmatch(r"\d+", line):
                res += int(line)
                break
            if m := re.search(r"\((\d+)\)", line):
                line = line[:m.start()] + m.group(1) + line[m.end():]
            elif m:= next(line):
                if m.group(2) == "+":
                    value = int(m.group(1)) + int(m.group(3))
                    line = line[:m.start()] + str(value) + line[m.end():]
                else:
                    value = int(m.group(1)) * int(m.group(3))
                    line = line[:m.start()] + str(value) + line[m.end():]
            else:
                raise Exception(line)
    return res

class TreeTwo:
    """
    Grammar:
        E => T | E*T
        T => F | T+F
        F => (E) | \d+

    Grammar without left recursion:
        E => T Eb
        Eb => + T Eb | ε
        T => F Tb
        Tb => * F Tb | ε
        F => ( E ) | \d+
    """
    def __init__(self, line):
        self.tokens = re.findall("\d+|[()+-/*]", line)
        self.pos = 0
    
    def accept(self, regex, raise_on_false=False):
        if self.pos >= len(self.tokens):
            return False
        if re.fullmatch(regex, self.tokens[self.pos]):
            self.pos += 1
            return True
        if raise_on_false:
            print(self.tokens, self.pos)
            raise Exception(f"regex: {regex} do not match {self.tokens[self.pos]}")
        return False

    def E(self):
        T = self.T()
        Eb = self.Eb()
        return T * Eb

    def Eb(self):
        if self.accept(r"\*"):
            T = self.T()
            Eb = self.Eb()
            return T * Eb
        else:
            return 1
    
    def T(self):
        F = self.F()
        Tb = self.Tb()
        return F + Tb

    def Tb(self):
        if self.accept(r"\+"):
            F = self.F()
            Tb = self.Tb()
            return F + Tb
        else:
            return 0

    def F(self):
        if self.accept(r"\("):
            E = self.E()
            self.accept(r"\)", raise_on_false=True)
            return E
        elif self.accept(r"\d+", raise_on_false=True):
            return int(self.tokens[self.pos-1])

def partTwoBis(lines):
    res = 0
    for line in lines:
        res += TreeTwo(line).E()
    return res

if __name__=="__main__":
    trees = parseOne("input")
    print("PartOne: {}".format(partOne(trees)))

    lines = parseTwo("input")
    print("PartTwo: {}".format(partTwo(lines)))
    #lines = ["1 + 2 * 3 + 4 * 5 + 6"]
    print("PartTwoBis: {}".format(partTwoBis(lines)))
