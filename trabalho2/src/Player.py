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
        self.guess = None
        self.guessings = {i: None for i in range(1, 5)}
        self.players_alive = [i for i in range(1, 5)]
        self.still_to_guess = [i for i in range(1, 5)]
        self.guessing_sums = 0
        self.msg_to_send = Queue()
        self.manager = id == 1
        self.waiting_for_response = False
        self.passing_baston = False
        self.manager_id = None

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
    Set the baston to false
    '''
    def set_baston_to_false(self):
        self.baston = False

    '''
    Set the baston to true
    '''
    def set_baston_to_true(self):
        self.baston = True

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
    Put a message in the first position of the queue
    '''
    def put_msgs_first(self, msgs):
        with self.msg_to_send.mutex:
            for msg in reversed(msgs):
                self.msg_to_send.queue.appendleft(msg)

    '''
    Return the next message to send and pop it
    '''
    def get_next_msg(self):
        if not self.msg_to_send.empty():
            return self.msg_to_send.get()
        return None
    
    '''
    Remove a card from the player cards and return it
    '''
    def play_card(self, card_number):
        return self.cards.pop(card_number)

    '''
    Set the player's guess
    '''
    def set_guess(self, guess):
        self.guess = guess

    '''
    Get the player's guess
    '''
    def get_guess(self):
        return self.guess

    '''
    Set the manager id of the game
    '''
    def set_manager_id(self, manager_id):
        self.manager_id = manager_id

    '''
    Kill a player
    '''
    def kill_player(self, player_id):
        self.players_alive.remove(player_id)

    '''
    Add a player's guessing
    '''
    def add_player_guessing(self, player_id, guessing):
        if player_id == self.id:
            self.set_guess(guessing)

        self.guessings[player_id] = int(guessing)
        self.still_to_guess.remove(player_id)
        self.guessing_sums += int(guessing)
    
    '''
    Return 1 if the player is the last player to guess
    '''
    def last_player_to_guess(self):
        if len(self.still_to_guess) == 1 and self.still_to_guess[0] == self.id:
            return 1
        return 0
    
    '''
    Return 1 if the guess is available, 0 if not
    '''
    def validate_guess(self, guessing):
        if self.last_player_to_guess():
            if self.guessing_sums + int(guessing) == len(self.players_alive):
                return 0
            
        return 1
