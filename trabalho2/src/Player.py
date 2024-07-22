from .Card import Card

from queue import Queue

class Player:
    def __init__(self, id):
        self.id = id
        self.ports = self.set_ports()
        self.addr1 = ("localhost", self.ports[0])
        self.addr2 = ("localhost", self.ports[1])
        self.cards = []
        self.baston = True if id == 1 else False
        self.guessing = -1
        self.n_cards = 5
        self.msg_to_send = Queue()
        self.manager = True if id == 1 else False

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
    Invert the state of baston
    '''
    def invert_baston(self):
        self.baston = not self.baston

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
    
    '''
    Return the next player id
    '''
    def get_next_player(self):
        return self.id + 1 if self.id < 4 else 1
