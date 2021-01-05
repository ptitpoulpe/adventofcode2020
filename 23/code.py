#!/usr/bin/env python3

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    @staticmethod 
    def generate(cups):
        access = [None] * (len(cups) + 1)
        first = Node(cups[0])
        access[first.value] = first
        prev = first
        for cup in cups[1:]:
            current = Node(cup)
            access[current.value] = current
            prev.next = current
            prev = current
        prev.next = first
        return access

    def __str__(self):
        current = self.next
        res = [str(self.value)]
        while current != self:
            res.append(str(current.value))
            current = current.next
        return "".join(res)


def compute(cups, n):
    cups_nodes = Node.generate(cups)
    current_node = cups_nodes[cups[0]]

    for i in range(n):
        # Remove
        next1_node = current_node.next
        next2_node = next1_node.next
        next3_node = next2_node.next
        current_node.next = next3_node.next

        # Find where to insert
        next_values = [next1_node.value, next2_node.value, next3_node.value]
        insert = current_node.value
        stop = False
        while not stop:
            if insert == 1:
                insert = len(cups)
            else:
                insert -= 1
            stop = insert not in next_values

        # Insert
        insert_node = cups_nodes[insert]
        next3_node.next = insert_node.next
        insert_node.next = next1_node

        current_node = current_node.next

    return cups_nodes


def partOne(cups):
    cups_nodes = compute(cups, 100)

    one = cups_nodes[1]
    current = one.next
    res = []
    while current != one:
        res.append(str(current.value))
        current = current.next
    return "".join(res)


def partTwo(cups):
    cups_nodes = compute(cups, 10 ** 7)
    one = cups_nodes[1]
    return one.next.value * one.next.next.value


if __name__=="__main__":
    cups = [9,5,2,4,3,8,7,1,6]
    print("PartOne: {}".format(partOne(cups)))

    cups = cups + list(range(10, 10**6 + 1))
    print("PartTwo: {}".format(partTwo(cups)))
