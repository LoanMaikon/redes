from Card import Card
import random

class Deck:
    def __init__(self):
        self.values_power, self.suits_power = self.get_default_power_order()
        self.deck = self.create_deck()

    '''
    Compare two cards. Return 1 if card1 is better, 2 if card2 is better and 0 if they are equal
    '''
    def compare_cards(self, card1, card2):
        value1 = card1.get_value()
        value2 = card2.get_value()

        if self.values_power.index(value1) > self.values_power.index(value2):
            return 1
        elif self.values_power.index(value1) < self.values_power.index(value2):
            return 2
        return 0

    '''
    Draw n cards from the deck
    '''
    def draw_cards(self, n):
        drawn_cards = []
        for _ in range(n):
            drawn_cards.append(self.deck.pop())
        return drawn_cards

    '''
    Receive the turned_card and order the power of the cards by the shackle rule
    '''
    def order_power_by_shackle(self, turned_card):
        turned_card_index = self.values_power.index(turned_card.get_value())
        shackle_index = turned_card_index + 1
        if shackle_index == len(self.values_power):
            shackle_index = 0
        
        shackle = self.values_power[shackle_index]

        del self.values_power[shackle_index]
        self.values_power.append(shackle)

    '''
    Set the power order of the cards
    '''
    def get_default_power_order(self):
        # Values and suits ordered by power. The first is the worst and the last is the best.
        values_power = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        suits_power = ['Diamonds', 'Spades', 'Hearts', 'Clubs']

        return values_power, suits_power

    '''
    Restore the power order of the cards
    '''
    def reset_power_order(self):
        self.values_power, self.suits_power = self.get_default_power_order()

    '''
    Create the deck based on all possible values and suits
    '''
    def create_deck(self):
        deck = []
        for value in self.values_power:
            for suit in self.suits_power:
                deck.append([value, suit])
        
        return deck

    '''
    Shuffle the deck of cards
    '''
    def shuffle_deck(self):
        random.shuffle(self.cards)
