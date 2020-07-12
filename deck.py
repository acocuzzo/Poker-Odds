import card
import random
import numpy as np


class Deck(object):
    def __init__(self):
        self.remaining = 52
        self.cards = np.array(
            [card.Card(suit, val) for val in range(1, 14)
             for suit in card.Suit], dtype=object)

    def draw_card_at_idx(self, idx):
        # check if last card
        if idx != self.remaining - 1:
            # swap card positions
            self.cards[idx], self.cards[self.remaining - 1] = \
                self.cards[self.remaining - 1], self.cards[idx]
        self.remaining -= 1
        return self.cards[self.remaining]

    def draw_random_card(self):
        rand_idx = random.randint(0, self.remaining - 1)
        return self.draw_card_at_idx(rand_idx)
    
    def draw_card(self, this_card):
        for idx in range(self.remaining):
            if self.cards[idx] == this_card:
                return self.draw_card_at_idx(idx)
        return None
    
    def draw_card_of_suit(self, this_suit):
        for idx in range(self.remaining):
            if self.cards[idx].suit == this_suit:
                return self.draw_card_at_idx(idx)
        return None

    def draw_card_of_value(self, this_value):
        for idx in range(self.remaining):
            if self.cards[idx].value == this_value:
                return self.draw_card_at_idx(idx)
        return None
     
    def suit_count(self, this_suit):
        suit_count = 0
        while suit_count < 14:
            for idx in range(self.remaining):
                if self.cards[idx].suit == this_suit:
                    suit_count += 1
        return suit_count

    def value_count(self, this_value):
        value_count = 0
        while value_count < 5:
            for idx in range(self.remaining):
                if self.cards[idx].suit == this_value:
                    value_count += 1
        return value_count
    
    def get_remaining_cards(self):
        return self.cards[:self.remaining]

    def has_card(self, this_card):
        for idx in range(self.remaining):
            if self.cards[idx] == this_card:
                return True
        return False
