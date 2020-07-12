import enum
import numpy as np


class Suit(enum.IntEnum):
    Diamond = 0
    Heart = 1
    Club = 2
    Spade = 3


class Card(object):
    __slots__ = ('suit', 'value')

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __hash__(self):
        return hash((self.suit, self.value))

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __ne__(self, other):
        return not (self == other)

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
