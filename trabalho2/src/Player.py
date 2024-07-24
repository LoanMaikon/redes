from .Card import Card

from queue import Queue

class Player:
    def __init__(self, id):
        self.id = id
        self.ports = self.set_ports()
        self.addr1 = ("localhost", self.ports[0])
        self.addr2 = ("localhost", self.ports[1])
        self.cards = []
        self.baston = id == 1
        self.n_cards = 5
        self.msg_to_send = Queue()
        self.manager = id == 1

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
    Set the player cards from a json
    '''
    def set_cards_from_json(self, cards):
        self.cards = [Card(card[0], card[1]) for card in cards]
    
    '''
    Return the string of the player cards
    '''
    def get_str_cards(self):
        return ''.join([card.get_str_card() for card in self.cards])
    
    '''
    Return the next player id
    '''
    def get_next_player(self, n):
        next_player = self.id + n
        while next_player > 4:
            next_player -= 4

        return next_player
    
    '''
    Put a message in the queue
    '''
    def put_msg(self, msg):
        self.msg_to_send.put(msg)

    '''
    Return the next message to send and pop it
    '''
    def get_next_msg(self):
        if not self.msg_to_send.empty():
            return self.msg_to_send.get()
        return None
