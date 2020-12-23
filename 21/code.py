#!/usr/bin/env python3
import re
from collections import defaultdict

def parse(path):
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                m = re.fullmatch("(.*) \(contains (.*)\)", line)
                yield m.group(1).split(" "), m.group(2).split(", ")


def compute(foods):
    alergen_ingredientss = defaultdict(list)
    for ingredients, alergens in foods:
        ingredients = set(ingredients)
        for alergen in alergens:
            alergen_ingredientss[alergen].append(ingredients)
    
    matches = {}
    stabilized = False
    while not stabilized:
        stabilized = True
        for alergen, ingredientss in alergen_ingredientss.items():
            possibilities = set.intersection(*ingredientss) - matches.keys()
            if len(possibilities) == 1:
                matches[possibilities.pop()] = alergen
                stabilized = False 
    return matches


def partOne(foods):  
    matches = compute(foods)
    
    count = 0
    for ingredients, alergens in foods:
        for ingredient in ingredients:
            if ingredient not in matches:
                count +=1
    return count


def partTwo(foods):
    matches = compute(foods)
    return ",".join(sorted(matches, key=lambda x: matches[x]))


if __name__=="__main__":
    foods = list(parse("input"))
    print("PartOne: {}".format(partOne(foods)))
    print("PartTwo: {}".format(partTwo(foods)))
