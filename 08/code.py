#!/usr/bin/env python3
import re
from collections import defaultdict
from functools import lru_cache


def parse(path):
    instructions = []
    with open(path) as f:
        for line in f.read().split("\n"):
            if not line:
                continue
            op, arg = line.split()
            arg = int(arg)
            instructions.append((op, arg))
    return instructions


def run(program):
    accumulator = 0
    index = 0
    while True:
        op, arg = program[index]
        if op == "acc":
            accumulator += arg
        elif op == "nop":
            pass
        elif op == "jmp":
            index += arg - 1
        else:
            raise Exception("Op {} not handeled".format(op))
        index += 1
        yield accumulator, index

def partOne(program):
    done = set()
    for accumulator, index in run(program):
        if index in done:
            break
        done.add(index)
    return accumulator


def partTwo(program):
    finish = len(program)
    for i in range(len(program)):
        op, arg = program[i]
        op = "nop" if op == "jmp" else \
             "jmp" if op == "nop" else \
             op

        fixed_program = program.copy()
        fixed_program[i] = (op, arg)

        done = set()
        for accumulator, index in run(fixed_program):
            if index == finish:
                return accumulator
            if index in done:
                break
            done.add(index)


if __name__=="__main__":
    program = parse("input")

    print("PartOne: {}".format(partOne(program)))
    print("PartTwo: {}".format(partTwo(program)))