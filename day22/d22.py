#! /usr/bin/env python3


def read(fname):
    with open(fname, "r") as f:
        players = f.read().split("\n\n")

    decks = []
    for player in players:
        decks.append([int(v) for v in player.split("\n")[1:] if v != ""])
    return decks


def combat(deck1, deck2):
    while len(deck1) > 0 and len(deck2) > 0:
        d1_card = deck1.pop(0)
        d2_card = deck2.pop(0)
        if d1_card > d2_card:
            deck1.extend([d1_card, d2_card])
        elif d2_card > d1_card:
            deck2.extend([d2_card, d1_card])
        else:
            raise RuntimeError("Tie! {d1_card} for {deck1} and {deck2}")

    return deck1 if len(deck2) == 0 else deck2


def recursive_combat(deck1, deck2):
    """return (winner, winner_deck) where winner is true if player 1 won"""
    p1_seen_decks = set()
    p2_seen_decks = set()

    while len(deck1) > 0 and len(deck2) > 0:
        # if either of the decks have been seen before, p1 wins
        if tuple(deck1) in p1_seen_decks or tuple(deck2) in p2_seen_decks:
            return True, deck1
        else:
            p1_seen_decks.add(tuple(deck1))
            p2_seen_decks.add(tuple(deck2))

        d1_card = deck1.pop(0)
        d2_card = deck2.pop(0)

        if d1_card <= len(deck1) and d2_card <= len(deck2):
            p1_won, _ = recursive_combat(deck1[:d1_card], deck2[:d2_card])
        else:
            p1_won = d1_card > d2_card

        if p1_won:
            deck1.extend([d1_card, d2_card])
        else:
            deck2.extend([d2_card, d1_card])

    return len(deck2) == 0, deck1 if len(deck2) == 0 else deck2


def calculate_score(deck):
    return sum([i * v for i, v in enumerate(reversed(deck), start=1)])


print(calculate_score(combat(*read("input.txt"))))

p1_won, deck = recursive_combat(*read("input.txt"))
print(calculate_score(deck))
