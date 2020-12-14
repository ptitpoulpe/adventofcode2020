#!/usr/bin/env python3
import re


class Mask:
    def __init__(self, value):
        self.value = value
        self.zero = int(value.replace("X", "0"), base=2)
        self.one = int(value.replace("X", "1"), base=2)

    def mask(self, value):
        return (value & self.one ) | self.zero
    
    def all(self, value):
        value = value | self.zero
        values = [value]
        for i, x in enumerate(reversed(self.value)):
            if x == "X":
                new_values = []
                for value in values:
                    new_values.append(value | 2**i)
                    new_values.append(value & (2**36 - 1 - 2**i))
                values = new_values
        return values

class Mem:
    def __init__(self, address,  value):
        self.address = address
        self.value = value


MASK_RE = re.compile("^mask = ([0-9X]+)$")
MEM_RE = re.compile("^mem\[(\d+)\] = (\d+)$")
def parse(path):
    with open(path) as f:
        for line in f.readlines():
            if (m := MASK_RE.match(line)):
                yield Mask(m.group(1))
            elif (m := MEM_RE.match(line)):
                yield Mem(int(m.group(1)), int(m.group(2)))
            else:
                print("err", line)


def partOne(instructions):
    mask = Mask("X")
    memory = {}
    for instruction in instructions:
        if isinstance(instruction, Mask):
            mask = instruction
        elif isinstance(instruction, Mem):
            memory[instruction.address] = mask.mask(instruction.value)
    return sum(memory.values())


def partTwo(instructions):
    mask = Mask("0")
    memory = {}
    for instruction in instructions:
        if isinstance(instruction, Mask):
            mask = instruction
        elif isinstance(instruction, Mem):
            for address in mask.all(instruction.address):
                memory[address] = instruction.value
    return sum(memory.values())

if __name__=="__main__":
    instructions = list(parse("input"))

    print("PartOne: {}".format(partOne(instructions)))
    print("PartTwo: {}".format(partTwo(instructions)))