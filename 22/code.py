#!/usr/bin/env python3

def parse(path):
    with open(path) as f:
        return [
            [int(line) for line in player.split("\n")[1:] if line]
            for player in f.read().split("\n\n")
        ]


def partOne(players):
    player1, player2 = players
    while player1 and player2:
        player1_card = player1.pop(0)
        player2_card = player2.pop(0)
        if player1_card > player2_card:
            player1.append(player1_card)
            player1.append(player2_card)
        else:
            player2.append(player2_card)
            player2.append(player1_card)

    winner = player1 if player1 else player2
    return sum(v * (i + 1) for i, v in enumerate(reversed(winner)))


def game(player1, player2, indent=0):
    games = set()
    while player1 and player2:
        player1_card = player1.pop(0)
        player2_card = player2.pop(0)

        # Avoid recursion
        sig = f"{player1_card}: {player1} / {player2_card}: {player2}"
        if sig in games:
            return player1 + player2, []
        else:
            games.add(sig)

        #print(" "*indent, player1_card, player2_card, player1, player2)
        if player1_card <= len(player1) and player2_card <= len(player2):
            result = game(player1[:player1_card], player2[:player2_card], indent + 1)
            player1_win = len(result[0]) > len(result[1])
        else:
            player1_win = player1_card > player2_card
        #print(" "*indent, player1_card, player2_card, player1_win)
        if player1_win:
            player1.append(player1_card)
            player1.append(player2_card)
        else:
            player2.append(player2_card)
            player2.append(player1_card)
    return player1, player2 


def partTwo(players):
    player1, player2 = players
    player1, player2 = game(player1, player2)
    winner = player1 if player1 else player2
    return sum(v * (i + 1) for i, v in enumerate(reversed(winner)))


if __name__=="__main__":
    players = list(parse("input"))
    print("PartOne: {}".format(partOne(players)))
    players = list(parse("input"))
    print("PartTwo: {}".format(partTwo(players)))
