class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
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
    Return the string of the card
    card = [value, suit]
    '''
    def get_str_card(self):
        return self.value + ' of ' + self.suit + '\n'
    
    '''
    Transform a card in a list
    '''
    def to_list(self):
        return [self.value, self.suit]
    

    
