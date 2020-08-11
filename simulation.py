from game import Game
from deck import Deck
from card import Card, Suit
from hand import Result, Hand, check_is_straight


def generate_all_pockets():
    for val1 in range(13, 0, -1):
        for val2 in range(1, val1 + 1):
            if val1 != val2:
                yield [Card(Suit.Heart, val1), Card(Suit.Heart, val2)]
            yield [Card(Suit.Heart, val1), Card(Suit.Diamond, val2)]
    

def get_odds_dict(num_simulations, player_pocket, board, num_players):
    results = [0., 0., 0.]
    board_odds_by_rank = [0.] * 11
    same_pocket = 0
    share_one_card = 0
    using_board_hand = 0
    tie_count = 0
    delta = 1. / num_simulations
    full_deck = Deck()
    for _ in range(num_simulations):
        simulation = Game(num_players - 1, full_deck)
        simulation.set_player_pocket(player_pocket[0], player_pocket[1])
        simulation.set_board(board)
        res = simulation.run()
        # DEBUGGING ONLY:
        board_hand = Hand(simulation.board)
        board_hand.set_rank()
        if board_hand.rank < 10:
            board_odds_by_rank[board_hand.rank] += delta
        else:
            board_odds_by_rank[10] += delta
        if res == Result.Tie:
            tie_count += 1
            if simulation.get_best_opponent_hand() == board_hand and simulation.get_best_player_hand() == board_hand:
                using_board_hand += 1
            opp_pocket = simulation.opponent_pockets[0]
            if (player_pocket[0].value == opp_pocket[0].value or player_pocket[0].value == opp_pocket[1].value) and (player_pocket[1].value == opp_pocket[0].value or player_pocket[1].value == opp_pocket[1].value):
                same_pocket += 1
            if player_pocket[0].value == opp_pocket[0].value or player_pocket[0].value == opp_pocket[1].value:
                share_one_card += 1
        results[int(res)] += delta
        full_deck.remaining = 52
    print(board_odds_by_rank)
    print(tie_count)
    print(float(using_board_hand)/tie_count)
    print(float(same_pocket)/tie_count)
    print(float(share_one_card)/tie_count)
    return results


def generate_all_preflop_odds(num_simulations, num_players):
    output_file = open(
        '/home/anna/code/poker_python/preflop_results_trial6.txt', 'a+')
    for player_pocket in generate_all_pockets():
        odds_dict = get_odds_dict(num_simulations, player_pocket, [],
                                  num_players)
        output_file.write((','.join(
            map(str, [
                player_pocket[1], player_pocket[0], odds_dict[0], odds_dict[2],
                odds_dict[1]
            ]))) + "\n")
    output_file.close()


def main():
    generate_all_preflop_odds(10000, 2)