from util import read_input, safe_split


def calc_score(deck):
    return sum((len(deck) - i) * card for i, card in enumerate(deck))


def get_winning_deck(decks):
    return next(filter(None, decks))


def rec_combat(decks, upper_game=False):
    seen_before = set()
    while all(decks):
        deck_tuple = tuple(map(tuple, decks))
        if deck_tuple in seen_before:
            return 0, calc_score(decks[0]) if upper_game else None
        seen_before.add(deck_tuple)

        cards_drawn = [deck[0] for deck in decks]
        decks = [deck[1:] for deck in decks]

        if all(len(deck) >= card for deck, card in zip(decks, cards_drawn)):
            round_winner, _ = rec_combat([deck[:card] for deck, card in zip(decks, cards_drawn)])
        else:
            round_winner = cards_drawn.index(max(cards_drawn))

        spoils = [cards_drawn[round_winner]] + cards_drawn[:round_winner] + cards_drawn[round_winner + 1:]
        decks[round_winner] += spoils
    game_winner_deck = get_winning_deck(decks)
    return decks.index(game_winner_deck), calc_score(game_winner_deck) if upper_game else None


def combat(decks):
    while all(decks):
        cards_drawn = [deck[0] for deck in decks]
        decks = [deck[1:] for deck in decks]
        round_winner = cards_drawn.index(max(cards_drawn))
        spoils = [cards_drawn[round_winner]] + cards_drawn[:round_winner] + cards_drawn[round_winner + 1:]
        decks[round_winner] += spoils
    return calc_score(get_winning_deck(decks))


def parse_decks(text):
    return [[int(nr_str) for nr_str in safe_split(deck_text, '\n')[1:]]
            for deck_text in safe_split(text, '\n\n')]


def part1():
    return combat(parse_decks(read_input()))


def part2():
    return rec_combat(parse_decks(read_input()), upper_game=True)[1]


if __name__ == '__main__':
    print(part1())
    print(part2())
