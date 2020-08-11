import enum
import pdb


def check_is_flush(hand):
    first_suit = hand.cards[0].suit
    for c in hand.cards:
        if c.suit != first_suit:
            return False
    hand.tie_breakers = hand.get_tie_breakers_all_cards()
    hand.rank = 5
    return True


def check_is_straight(hand):
    idx = 0
    # ace case
    if hand.cards[idx].value == 1:
        idx += 1
        if hand.cards[idx].value != 2 and hand.cards[idx].value != 10:
            return False
    prev_val = hand.cards[idx].value
    idx += 1
    while idx != 5:
        curr_val = hand.cards[idx].value
        if curr_val != prev_val + 1:
            return False
        prev_val = curr_val
        idx += 1
    hand.tie_breakers = hand.get_tie_breakers_all_straights()
    hand.rank = 6
    return True


def check_is_royal_flush(hand):
    if not hand.has_value(1):
        return False
    for val in range(10, 14):
        if not hand.has_value(val):
            return False
    if check_is_flush(hand):
        hand.tie_breakers = [1]
        hand.rank = 1
        return True
    return False


def check_is_straight_flush(hand):
    if check_is_straight(hand) and check_is_flush(hand):
        hand.tie_breakers = hand.get_tie_breakers_all_straights()
        hand.rank = 2
        return True
    return False


def check_has_four_of_kind(hand):
    value_count = [0] * 14
    four_val = 0
    single_value = 0
    for c in hand.cards:
        value_count[c.value] += 1
    for val in range(1, 14):
        if value_count[val] == 1:
            single_value = val
        if value_count[val] == 4:
            four_val = val
    if four_val != 0:
        hand.tie_breakers = [convert_value_to_rank(v) for v in [four_val, single_value]]
        hand.rank = 3
        return True
    return False


def check_is_full_house(hand):
    value_count = [0] * 14
    triple_value = 0
    pair_value = 0
    for c in hand.cards:
        value_count[c.value] += 1
    for val in range(1, 14):
        if value_count[val] == 3:
            triple_value = val
        if value_count[val] == 2:
            pair_value = val
    if triple_value != 0 and pair_value != 0:
        hand.tie_breakers = [convert_value_to_rank(v) for v in [triple_value, pair_value]]
        hand.rank = 4
        return True
    return False


def check_has_three_of_kind(hand):
    value_count = [0] * 14
    triple_value = 0
    single_values = []
    for c in hand.cards:
        value_count[c.value] += 1
    for val in range(1, 14):
        if value_count[val] == 3:
            triple_value = val
        elif value_count[val] == 2:
            return False
        elif value_count[val] == 1:
            single_values.append(val)
    if triple_value != 0 and len(single_values) == 2:
        single_ranks = [convert_value_to_rank(v) for v in single_values]
        single_ranks.sort()
        hand.tie_breakers = [
            convert_value_to_rank(triple_value),
            single_ranks[0],
            single_ranks[1]
        ]
        hand.rank = 7
        return True
    return False


def check_has_two_pair(hand):
    value_count = [0] * 14
    pair_values = []
    single_value = 0
    for c in hand.cards:
        value_count[c.value] += 1
    for val in range(1, 14):
        if value_count[val] > 2:
            return False
        if value_count[val] == 1:
            single_value = val
        elif value_count[val] == 2:
            pair_values.append(val)
    if len(pair_values) == 2:
        pair_ranks = [convert_value_to_rank(v) for v in pair_values]
        pair_ranks.sort()
        hand.tie_breakers = [
            pair_ranks[0], pair_ranks[1],
            convert_value_to_rank(single_value)
        ]
        hand.rank = 8
        return True
    return False


def check_has_one_pair(hand):
    value_count = [0] * 14
    for c in hand.cards:
        value_count[c.value] += 1
    pair_value = 0
    single_values = []
    for val in range(1, 14):
        if value_count[val] > 2:
            return False
        if value_count[val] == 2:
            if pair_value != 0:
                return False
            pair_value = val
        elif value_count[val] == 1:
            single_values.append(val)
    if pair_value != 0 and len(single_values) == 3:
        single_ranks = [convert_value_to_rank(v) for v in single_values]
        single_ranks.sort()
        hand.tie_breakers = [convert_value_to_rank(pair_value),
                             single_ranks[0],
                             single_ranks[1],
                             single_ranks[2]
                             ]
        hand.rank = 9
        return True
    return False


HAND_CHECKS = [
    check_is_royal_flush, check_is_straight_flush, check_has_four_of_kind,
    check_is_full_house, check_is_flush, check_is_straight,
    check_has_three_of_kind, check_has_two_pair, check_has_one_pair
]


class Result(enum.IntEnum):
    Win = 0
    Lose = 1
    Tie = 2


def convert_value_to_rank(value):
    if value == 1:
        return 1
    return 15 - value


class Hand(object):
    def __init__(self, cards):
        assert len(cards) == 5
        self.cards = cards
        self.cards.sort()
        self.rank = 0
        self.tie_breakers = []

    def __eq__(self, other):
        return self.cards == other.cards

    def __hash__(self):
        return hash(tuple(self.cards))

    def __str__(self):
        return str(self.cards[0]) + " " + str(self.cards[1]) + " " + str(
            self.cards[2]) + " " + str(self.cards[3]) + " " + str(
                self.cards[4])

    def get_cards(self):
        return self.cards

    def get_tie_breakers(self):
        return self.tie_breakers

    def get_tie_breakers_all_straights(self):
        # if ace is high
        if self.cards[0].value == 1 and self.cards[1].value != 2:
            return [1]
        # otherwise ace is low or not present, return high_card_rank
        return [convert_value_to_rank(self.cards[4].value)]

    def get_tie_breakers_all_cards(self):
        idx = 0
        tie_breakers = []
        # if lowest card is an ace
        if self.cards[0].value == 1:
            tie_breakers.append(1)
            idx += 1
        # go from highest card to lowest, skip if lowest is ace
        for n in range(4, idx - 1, -1):
            tie_breakers.append(convert_value_to_rank(self.cards[n].value))
        return tie_breakers

    def compare_tie_breakers(self, other):
        if self.rank == 1:
            return Result.Tie
        # straight flush, straights check only one tie_breaker
        if self.rank == 2 or self.rank == 6:
            if self.tie_breakers[0] < other.tie_breakers[0]:
                return Result.Win
            if self.tie_breakers[0] > other.tie_breakers[0]:
                return Result.Lose
            for idx in range(5):
                assert self.cards[idx].value == other.cards[idx].value
            return Result.Tie
        # compare elements in order
        for idx in range(len(self.tie_breakers)):
            if self.tie_breakers[idx] < other.tie_breakers[idx]:
                return Result.Win
            if self.tie_breakers[idx] > other.tie_breakers[idx]:
                return Result.Lose
        for idx in range(5):
            assert self.cards[idx].value == other.cards[idx].value
        return Result.Tie

    def has_card(self, this_card):
        return this_card in self.cards

    def has_suit(self, suit):
        for c in self.cards:
            if c.suit == suit:
                return True
        return False

    def has_value(self, value):
        for c in self.cards:
            if c.value == value:
                return True
            if c.value > value:
                return False
        return False

    def get_high_card_rank(self):
        if self.cards[0].value == 1:
            return 1
        return convert_value_to_rank(self.cards[4].value)

    def set_rank(self):
        if self.rank != 0:
            return
        # each fn in check_list sets rank and tiebreakers
        for fn in HAND_CHECKS:
            if fn(self):
                return
        self.rank = self.get_high_card_rank() + 9
        self.tie_breakers = self.get_tie_breakers_all_cards()

    def get_rank(self):
        return self.rank

    def compare_with(self, other):
        if self.rank < other.rank:
            return Result.Win
        if self.rank > other.rank:
            return Result.Lose
        return self.compare_tie_breakers(other)
