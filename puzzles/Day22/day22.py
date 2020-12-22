from util import read_input, safe_split


def calc_score(deck):
    return sum((len(deck) - i) * card for i, card in enumerate(deck))


def rec_combat(deck0, deck1):
    seen_before = set()
    while len(deck0) > 0 and len(deck1) > 0:
        deck_tuple = (tuple(deck0), tuple(deck1))
        if deck_tuple in seen_before:
            return 0, calc_score(deck0)
        else:
            seen_before.add(deck_tuple)
        card0, *deck0 = deck0
        card1, *deck1 = deck1
        if len(deck0) >= card0 and len(deck1) >= card1:
            round_winner, _ = rec_combat(deck0[:card0], deck1[:card1])
        else:
            round_winner = 0 if card0 > card1 else 1

        if round_winner == 0:
            deck0 += [card0, card1]
        else:
            deck1 += [card1, card0]
    game_winner = 1 if len(deck0) == 0 else 0
    return game_winner, calc_score(deck0 if game_winner == 0 else deck1)


def combat(deck0, deck1):
    while all(map(lambda l: len(l) > 0, [deck0, deck1])):
        card0, *deck0 = deck0
        card1, *deck1 = deck1
        if card0 > card1:
            deck0 += [card0, card1]
        else:
            deck1 += [card1, card0]
    return calc_score(deck0 if len(deck1) == 0 else deck1)


def parse_decks(text):
    return [[int(nr_str) for nr_str in safe_split(deck_text, '\n')[1:]]
            for deck_text in safe_split(text, '\n\n')]


def part1():
    return combat(*parse_decks(read_input()))


def part2():
    return rec_combat(*parse_decks(read_input()))[1]


if __name__ == '__main__':
    print(part1())
    print(part2())
