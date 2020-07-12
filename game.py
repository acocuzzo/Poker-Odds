from card import Card, Suit
from hand import Hand, Result
import enum
import copy
import line_profiler
import atexit
import numpy as np

profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)


class GameState(enum.IntEnum):
    Blinds = 0
    PreFlop = 1
    PostFlop = 2
    PostTurn = 3
    PostRiver = 4


@profile
def choose_n_cards_from_options(n, card_options):
    if n == 1:
        for c in card_options:
            def gen():
                yield c
            yield gen
    else:
        prev_result = choose_n_cards_from_options(n - 1, card_options)
        for r in prev_result:
            for c in card_options:
                not_duplicate = True
                for existing_card in r():
                    if c == existing_card:
                        not_duplicate = False
                if not_duplicate:
                    def gen():
                        for c1 in r():
                            yield c1
                        yield c
                    yield gen


class Game(object):
    def __init__(self, opponents, full_deck):
        self.state = GameState.Blinds
        self.opponents = opponents
        self.deck = full_deck
        # two cards
        self.player_pocket = []
        # list of hands
        self.player_hands = set()
        self.board = []
        self.opponent_pockets = [[]]
        # list of hands
        self.opponent_hands = set()

    def set_player_pocket(self, card1, card2):
        self.player_pocket = [self.deck.draw_card(card1),
                              self.deck.draw_card(card2)]
        self.state = GameState.PreFlop

    def set_board(self, list_of_cards):
        if len(list_of_cards) == 0:
            self.state = GameState.PreFlop
            return
        for c in list_of_cards:
            self.board.append(self.deck.draw_card(c))
        if len(list_of_cards) == 3:
            self.state = GameState.PostFlop
            return
        if len(list_of_cards) == 4:
            self.state = GameState.PostTurn
            return
        if len(list_of_cards) == 5:
            self.state = GameState.PostRiver
            return

    def set_flop(self, card1, card2, card3):
        if len(self.board) == 0:
            self.board.append(self.deck.draw_card(card1))
            self.board.append(self.deck.draw_card(card2))
            self.board.append(self.deck.draw_card(card3))
            self.state = GameState.PostFlop

    def set_turn(self, card1):
        if len(self.board) == 3:
            self.board.append(self.deck.draw_card(card1))
            self.state = GameState.PostTurn

    def set_river(self, card1):
        if len(self.board) == 4:
            self.board.append(self.deck.draw_card(card1))
            self.state = GameState.PostRiver

    def simulate_to_river(self):
        if int(self.state) < 1:
            self.player_pocket.append(self.deck.draw_random_card())
            self.player_pocket.append(self.deck.draw_random_card())
        if int(self.state) < 2:
            self.board.append(self.deck.draw_random_card())
            self.board.append(self.deck.draw_random_card())
            self.board.append(self.deck.draw_random_card())
        if int(self.state) < 3:
            self.board.append(self.deck.draw_random_card())
        if int(self.state) < 4:
            self.board.append(self.deck.draw_random_card())
        self.state = GameState.PostRiver

    @profile
    def build_hands(self, pocket, set_to_build,
                    num_from_pocket, num_from_board):
        for board_cards in choose_n_cards_from_options(num_from_board,
                                                       self.board):
            for pocket_cards in choose_n_cards_from_options(num_from_pocket, pocket):
                hand_list = []
                for c in board_cards():
                    hand_list.append(c)
                for c in pocket_cards():
                    hand_list.append(c)
                set_to_build.add(Hand(hand_list))
    
    @profile
    def set_player_hands(self):
        # 2 from pocket, 3 from board:
        self.build_hands(self.player_pocket, self.player_hands, 2, 3)
        # 1 from pocket, 4 from board:
        self.build_hands(self.player_pocket, self.player_hands, 1, 4)
        # 5 from board
        self.player_hands.add(Hand(self.board))
    
    def set_opponent_hands(self):
        for opp_pocket in self.opponent_pockets:
            # 2 from pocket, 3 from board:
            self.build_hands(opp_pocket, self.opponent_hands, 2, 3)
            # 1 from pocket, 4 from board:
            self.build_hands(opp_pocket, self.opponent_hands, 1, 4)
        # 5 from board
        self.opponent_hands.add(Hand(self.board))
    
    def set_all_hands(self):
        self.set_player_hands()
        self.set_opponent_hands()

    def set_all_ranks(self):
        if len(self.player_hands) == 0:
            return
        for h in self.player_hands:
            h.set_rank()
        if len(self.opponent_hands) == 0:
            return
        for h in self.opponent_hands:
            h.set_rank()

    def get_best_player_hand(self):
        best_hand = Hand([Card(Suit.Club, 7),
                          Card(Suit.Heart, 2),
                          Card(Suit.Heart, 3),
                          Card(Suit.Heart, 4),
                          Card(Suit.Heart, 5),
                          ])
        best_hand.rank = 30
        for h in self.player_hands:
            if h.get_rank() == 0:
                h.set_rank()
                assert h.get_rank() != 0, "this should not be possible"
            if h.compare_with(best_hand) == Result.Win:
                best_hand = h
        return best_hand

    def get_best_opponent_hand(self):
        best_hand = Hand([Card(Suit.Club, 7),
                          Card(Suit.Heart, 2),
                          Card(Suit.Heart, 3),
                          Card(Suit.Heart, 4),
                          Card(Suit.Heart, 5),
                          ])
        best_hand.rank = 30
        for h in self.opponent_hands:
            if h.get_rank() == 0:
                h.set_rank()
                assert(h.get_rank() != 0)
            if h.compare_with(best_hand) == Result.Win:
                best_hand = h
        return best_hand

    def run(self):
        if self.state != GameState.PostRiver:
            self.simulate_to_river()
        for _ in range(self.opponents):
            self.opponent_pockets.append([
                self.deck.draw_random_card(),
                self.deck.draw_random_card()
            ])
        self.set_all_hands()
        self.set_all_ranks()
        best_player_hand = self.get_best_player_hand()
        best_opponent_hand = self.get_best_opponent_hand()
        return best_player_hand.compare_with(best_opponent_hand)
