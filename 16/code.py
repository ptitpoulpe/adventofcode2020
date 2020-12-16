#!/usr/bin/env python3


def parse(path):
    with open(path) as f:
        rules = {}
        
        s_rules, s_my_ticket, s_nearby_tickets = f.read().split("\n\n")

        rules = {}
        for rule in s_rules.split("\n"):
            name, constraints = rule.split(":")
            rule = set()
            for constraint in constraints.split(" or "):
                cmin, cmax = constraint.split("-")
                rule |= {i for i in range(int(cmin), int(cmax) + 1)}
            rules[name] = rule

        my_ticket = [int(f) for f in s_my_ticket.split("\n")[1].split(",")]

        nearby_tickets = [
            [int(f) for f in ticket.split(",")]
            for ticket in s_nearby_tickets.split("\n")[1:]
            if ticket
        ]

        return rules, my_ticket, nearby_tickets


def partOne(rules, nearby_tickets):
    all_possible_values = set.union(
        *(possible_values
        for possible_values in rules.values())
    )
            
    errors = []
    for nearby_ticket in nearby_tickets:
        for field in nearby_ticket:
            if field not in all_possible_values:
                errors.append(field)
    return sum(errors)

def partTwo(rules, my_ticket, nearby_tickets):
    all_possible_values = set.union(
        *(possible_values
        for possible_values in rules.values())
    )

    valid_tickets = [
        ticket
        for ticket in nearby_tickets
        if all(field in all_possible_values for field in ticket)
    ]

    fields = []
    for values in zip(*valid_tickets):
        possible_fields = []
        for name, possible_values in rules.items():
            if all(value in possible_values for value in values):
                possible_fields.append(name)
        fields.append(possible_fields)
    
    while True:
        alones = [pf[0] for pf in fields if len(pf) == 1]
        if len(alones) == len(my_ticket):
            break
        for pf in fields:
            if len(pf) > 1:
                for alone in alones:
                    if alone in pf:
                        pf.remove(alone)
    res = 1
    for name, value in zip(fields, my_ticket):
        if name[0].startswith("departure"):
            res *= value
    return res


if __name__=="__main__":
    rules, my_ticket, nearby_tickets = parse("input")

    print("PartOne: {}".format(partOne(rules, nearby_tickets)))
    print("PartTwo: {}".format(partTwo(rules, my_ticket, nearby_tickets)))