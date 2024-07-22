from .Card import Card

class Player:
    def __init__(self, id):
        self.id = id
        self.ports = self.set_ports()
        self.addr1 = ("localhost", self.ports[0])
        self.addr2 = ("localhost", self.ports[1])
        self.cards = []

    '''
    Return the player id
    '''
    def get_id(self):
        return self.id
    
    '''
    Return the addr1
    '''
    def get_addr1(self):
        return self.addr1
    
    '''
    Return the addr2
    '''
    def get_addr2(self):
        return self.addr2

    '''
    Return the ports of the player
    '''
    def set_ports(self):
        all_ports = [[1917, 1918], [1918, 1919], [1919, 1920], [1920, 1917]]

        return all_ports[self.id - 1]
    
    '''
    Set the player cards
    '''
    def set_cards(self, cards):
        self.cards = cards
    
    '''
    Return the string of the player cards
    '''
    def get_str_cards(self, cards):
        return ''.join([card.get_str_card() for card in cards])
