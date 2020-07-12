import enum


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
    for c in hand.cards:
        value_count[c.value] += 1
    for val in range(1, 14):
        if value_count[val] == 4:
            hand.tie_breakers = [convert_value_to_rank(val)]
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
        hand.tie_breakers = [
            convert_value_to_rank(triple_value),
            convert_value_to_rank(pair_value)
        ]
        hand.rank = 4
        return True
    return False


def check_has_three_of_kind(hand):
    value_count = [0] * 14
    triple_value = 0
    has_no_pair = True
    for c in hand.cards:
        value_count[c.value] += 1
    for val in range(1, 14):
        if value_count[val] == 3:
            triple_value = val
        if value_count[val] == 2:
            has_no_pair = False
    if triple_value != 0 and has_no_pair:
        hand.tie_breakers = [convert_value_to_rank(triple_value)]
        hand.rank = 7
        return True
    return False


def check_has_two_pair(hand):
    value_count = [0] * 14
    pair_tie_breakers = []
    for c in hand.cards:
        value_count[c.value] += 1
    for val in range(1, 14):
        if value_count[val] > 2:
            return False
        if value_count[val] == 2:
            pair_tie_breakers.append(convert_value_to_rank(val))
    if len(hand.tie_breakers) == 2:
        hand.tie_breakers = pair_tie_breakers
        hand.rank = 8
        return True
    return False


def check_has_one_pair(hand):
    value_count = [0] * 14
    for c in hand.cards:
        value_count[c.value] += 1
    pair_value = 0
    for val in range(1, 14):
        if value_count[val] > 2:
            return False
        if value_count[val] == 2:
            if pair_value != 0:
                return False
            pair_value = val
    if pair_value != 0:
        hand.tie_breakers = [convert_value_to_rank(pair_value)]
        hand.rank = 9
        return True
    return False


HAND_CHECKS = [
    check_is_royal_flush,
    check_is_straight_flush,
    check_has_four_of_kind,
    check_is_full_house,
    check_is_flush,
    check_is_straight,
    check_has_three_of_kind,
    check_has_two_pair,
    check_has_one_pair
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
        # for c in cards:
            # assert (c.value < 14)
            # assert (c.value != 0)
            # assert (int(c.suit) < 4)
        self.cards = sorted(cards)
        self.rank = 0
        self.tie_breakers = []

    def __eq__(self, other):
        for idx in range(5):
            if self.cards[idx] != other.cards[idx]:
                return False
        return True
    
    def __hash__(self):
        return hash(tuple(self.cards,))

    def __str__(self):
        hand_string = ""
        for c in self.cards:
            hand_string += str(c) + ", "
        hand_string += "\n"
        return hand_string

    def get_cards(self):
        return self.cards

    def get_tie_breakers(self):
        return self.tie_breakers

    def get_tie_breakers_all_straights(self):
        # if ace is high
        if self.cards[0].value == 1 and self.cards[1].value != 2:
            return [convert_value_to_rank(1)]
        # otherwise ace is low or not present
        return [convert_value_to_rank(self.cards[4].value)]

    def get_tie_breakers_all_cards(self):
        return [
            convert_value_to_rank(self.cards[0].value),
            convert_value_to_rank(self.cards[1].value),
            convert_value_to_rank(self.cards[2].value),
            convert_value_to_rank(self.cards[3].value),
            convert_value_to_rank(self.cards[4].value),
        ]

    def compare_tie_breakers(self, other):
        if self.rank == 1:
            return Result.Tie
        # compare one value for StraightFlush,
        # FourofKind, Straights, Three of King, OnePair
        if self.rank == 2 or self.rank == 3 or self.rank == 6 or self.rank == 7 or self.rank == 9:
            if self.tie_breakers[0] < other.tie_breakers[0]:
                return Result.Win
            if self.tie_breakers[0] > other.tie_breakers[0]:
                return Result.Lose
            return Result.Tie
        # compare elements in order if Full House, Flush, Two Pair, High Card
        if self.rank == 4 or self.rank == 5 or self.rank == 8 or self.rank > 9:
            for idx in range(len(self.tie_breakers)):
                if self.tie_breakers[idx] < other.tie_breakers[idx]:
                    return Result.Win
                if self.tie_breakers[idx] > other.tie_breakers[idx]:
                    return Result.Lose
                return Result.Tie
        return Result.Tie

    def has_card(self, this_card):
        for c in self.cards:
            if c == this_card:
                return True
        return False

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
        self.tie_breakers = sorted(self.get_tie_breakers_all_cards())

    def get_rank(self):
        return self.rank

    def compare_with(self, other):
        if self.rank < other.rank:
            return Result.Win
        if self.rank > other.rank:
            return Result.Lose
        return self.compare_tie_breakers(other)
