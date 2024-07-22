import random

class Cards:
    def __init__(self):
        self.values_power, self.suits_power = self.get_default_power_order()
        self.deck = self.create_deck()

    '''
    Return the value of the card
    card = [value, suit]
    '''
    def get_value(self, card):
        return card[0]

    '''
    Return the suit of the card
    card = [value, suit]
    '''
    def get_suit(self, card):
        return card[1]

    '''
    Compare two cards. Return 1 if card1 is better, 2 if card2 is better and 0 if they are equal
    '''
    def compare_cards(self, card1, card2):
        value1 = self.get_value(card1)
        value2 = self.get_value(card2)

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
        shackle_index = self.values_power.index(turned_card.get_value(turned_card)) + 1 if turned_card.get_value(turned_card) != '3' else 0
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
        self.deck = []
        for value in self.values_power:
            for suit in self.suits_power:
                self.deck.append([value, suit])

    '''
    Shuffle the deck of cards
    '''
    def shuffle_deck(self):
        random.shuffle(self.cards)
