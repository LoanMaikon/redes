class Card():
    emojis = {
        'D': '♦️',
        'S': '♠️',
        'H': '♥️',
        'C': '♣️'
    }

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    '''
    Return the value of the card
    card = [value, suit]
    '''
    def get_value(self):
        return self.value

    '''
    Return the suit of the card
    card = [value, suit]
    '''
    def get_suit(self):
        return self.suit
    
    '''
    Transform a card in a list
    '''
    def to_list(self):
        return [self.value, self.suit]
    
    def __str__(self) -> str:
        return f'{self.value}{Card.emojis[self.suit]}'
