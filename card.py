import enum
import numpy as np


class Suit(enum.IntEnum):
    Diamond = 0
    Heart = 1
    Club = 2
    Spade = 3


CARDS = np.empty(52, dtype=object)


def Card(suit, value):
    return CARDS[int(suit) * 13 + value - 1]


class CardInternal(object):
    __slots__ = ('suit', 'value')

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __hash__(self):
        return hash((self.suit, self.value))

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        return self.suit < other.suit

    def __gt__(self, other):
        if self.value != other.value:
            return self.value > other.value
        return self.suit > other.suit

    def value_to_string(self):
        if self.value < 1:
            return "value cannot be less than 1"
        if self.value == 1:
            return "Ace"
        if self.value == 13:
            return "King"
        if self.value == 12:
            return "Queen"
        if self.value == 11:
            return "Jack"
        return str(self.value)

    def suit_to_string(self):
        if self.suit == Suit.Diamond:
            return "of Diamonds"
        if self.suit == Suit.Heart:
            return "of Hearts"
        if self.suit == Suit.Club:
            return "of Clubs"
        if self.suit == Suit.Spade:
            return "of Spades"

    def __str__(self):
        return self.value_to_string() + " " + self.suit_to_string()

    def __repr__(self):
        return self.value_to_string() + " " + self.suit_to_string()


for s in (Suit.Diamond, Suit.Heart, Suit.Spade, Suit.Club):
    for i in range(1, 14):
        CARDS[s * 13 + i - 1] = CardInternal(s, i)


class Pocket(object):
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort()

    def __eq__(self, other):
        return self.cards == other.cards

    def __ne__(self, other):
        return self.cards != other.cards

    def __hash__(self):
        return hash(tuple(self.cards))

    def __str__(self):
        return str(self.cards[0]) + ", " + str(self.cards[1])


# prevents duplicates by ignoring the suit
class PreFlop_Test_Pocket(object):
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort()

    def __eq__(self, other):
        return self.cards[0].value == other.cards[0].value(
        ) and self.cards[1] == other.cards[1].value

    def __ne__(self, other):
        return self.cards[0].value != other.cards[0].value(
        ) or self.cards[1].value != other.cards[1].value

    def __hash__(self):
        return hash(tuple(self.cards[0].value, self.cards[1].value))

    def __str__(self):
        return str(self.cards[0]) + ", " + str(self.cards[1])
