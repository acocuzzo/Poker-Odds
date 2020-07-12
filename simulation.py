from game import Game
from deck import Deck
from card import Card, Suit, PreFlop_Test_Pocket


def generate_all_pockets(full_deck):
    all_possible_pockets = set()
    for card_a in full_deck:
        for card_b in full_deck:
            if card_a != card_b:
                all_possible_pockets.add(PreFlop_Test_Pocket([card_a, card_b]))
    return all_possible_pockets


def generate_half_pockets():
    card_options = []
    for val in range(1, 14):
        card_options.append(Card(Suit.Diamond, val))
        card_options.append(Card(Suit.Heart, val))
    return generate_all_pockets(card_options)


def generate_pair_pockets():
    all_possible_pockets = set()
    for val in range(1, 14):
        all_possible_pockets.add(
            PreFlop_Test_Pocket(
                [Card(Suit.Diamond, val),
                 Card(Suit.Heart, val)]))
    return all_possible_pockets


def get_odds_dict(num_simulations, player_pocket, board, num_players):
    results = [0, 0, 0]
    full_deck = Deck()
    for _ in range(num_simulations):
        simulation = Game(num_players - 1, full_deck)
        simulation.set_player_pocket(player_pocket[0], player_pocket[1])
        simulation.set_board(board)
        results[int(simulation.run())] += 1
        full_deck.remaining = 52
    return [float(res) / float(num_simulations) for res in results]


def generate_all_preflop_odds(num_simulations, num_players):
    preflop_odds = {}
    for player_pocket in generate_half_pockets():
        preflop_odds[player_pocket] = get_odds_dict(num_simulations,
                                                    player_pocket.cards, [],
                                                    num_players)
        print(player_pocket)
        print(preflop_odds[player_pocket])
    return preflop_odds


def generate_preflop_odds_all_pairs(num_simulations, num_players):
    preflop_odds = {}
    for player_pocket in generate_pair_pockets():
        preflop_odds[player_pocket] = get_odds_dict(num_simulations,
                                                    player_pocket.cards, [],
                                                    num_players)
        print(player_pocket)
        print(preflop_odds[player_pocket])
    return preflop_odds


def main():
    player_pocket = [Card(Suit.Diamond, 13), Card(Suit.Heart, 13)]
    odds_dict = get_odds_dict(1000, player_pocket, [], 2)
    return odds_dict
