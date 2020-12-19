#!/usr/bin/env python3


def parse(path):
    with open(path) as f:
        rules_section, messages_section = f.read().split("\n\n")
        rules = {}
        for rule in rules_section.split("\n"):
            name, blocks = rule.split(": ")
            rules[int(name)] = blocks[1:-1] if '"' in blocks else \
                [
                    [int(elem) for elem in block.split(" ")]
                    for block in blocks.split(" | ")
                ]
        messages = [
            message 
            for message in messages_section.split("\n")
            if message]
        return rules, messages


def check(rules, rule, message, indent=0):
    possibilities = rules[rule]
    if isinstance(possibilities, str):
        if len(message) > 0 and message[0] == possibilities:
            return [message[1:]]
        else:
            return []
    else:
        res = []
        for possibility in possibilities:
            end_messages = [message]
            for value in possibility:
                end_messages = [
                    m
                    for end_message in end_messages
                    for m in check(rules, value, end_message, indent+1)
                ]
            res.extend(end_messages)
        return res


def partOne(rules, messages):
    count = 0
    for message in messages:
        for res in check(rules, 0, message):
            if len(res)==0:
                count += 1
                break
    return count


if __name__=="__main__":
    rules, messages = parse("input")
    print("PartOne: {}".format(partOne(rules, messages)))

    rules[8] =  [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    print("PartTwo: {}".format(partOne(rules, messages)))
