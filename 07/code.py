#!/usr/bin/env python3
import re
from collections import defaultdict
from functools import lru_cache


RULE_REGEX = re.compile("^(.*?) bags contain (.*?)$")
BAGS_REGEX = re.compile("(\d+) (.*?) bag")
def parse(path):
    rules = {}
    with open(path) as f:
        for line in f.read().split("\n"):
            if not line:
                continue
            bag, nbags_in = RULE_REGEX.match(line).groups()
            contain = []
            for n, bag_in in BAGS_REGEX.findall(nbags_in):
                contain.append((int(n), bag_in))
            rules[bag] = contain
    return rules



def partOne(rules):
    reverse = defaultdict(set)
    for bag, contains in rules.items():
        for _, bag_in in contains:
            reverse[bag_in].add(bag)

    shiny_gold_bags = set(reverse["shiny gold"])
    todo = list(shiny_gold_bags)
    while todo:
        bag = todo.pop()
        todo.extend(reverse[bag] - shiny_gold_bags)
        shiny_gold_bags |= reverse[bag]

    return len(shiny_gold_bags)


def partTwo(rules):
    @lru_cache
    def contains(bag):
        return 1 + sum(
            n * contains(bag_in) 
            for n, bag_in in rules[bag]
        )
    return contains("shiny gold") - 1


if __name__=="__main__":
    rules = parse("input")

    print("PartOne: {}".format(partOne(rules)))
    print("PartTwo: {}".format(partTwo(rules)))