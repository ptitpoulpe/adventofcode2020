#!/usr/bin/env python3


def parse(path):
    with open(path) as f:
        card_pub, door_pub, _ = f.read().split("\n")
        return int(card_pub), int(door_pub)


def loop(subject_number=7):
    value = 1
    divider = 20201227

    while True:
        value = value * subject_number
        value = value % divider
        yield value


def loop_size(pub):
    loop_size = 0
    for value in loop():
        loop_size += 1
        if value == pub:
            return loop_size


def loop_n(pub, n):
    for i, value in enumerate(loop(pub)):
        if i + 1 == n:
            return value


def partOne(card_pub, door_pub):
    card_loop_size = loop_size(card_pub)
    door_loop_size = loop_size(door_pub)

    enc_key_1 = loop_n(card_pub, door_loop_size)
    enc_key_2 = loop_n(door_pub, card_loop_size)
    assert(enc_key_1 == enc_key_2)

    return enc_key_1


if __name__=="__main__":
    card_pub, door_pub = parse("input")

    print("PartOne: {}".format(partOne(card_pub, door_pub)))
