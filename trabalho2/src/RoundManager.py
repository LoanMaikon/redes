from .Deck import Deck

class RoundManager:
    def __init__(self, manager_id):
        self.deck = Deck()
        self.manager_id = manager_id
        self.alive_players = [1, 2, 3, 4]
        self.round = 1

    '''
    Attributes go to the next round. Deck reseted
    '''
    def next_round(self):
        self.deck.reset_deck()
        self.round += 1

    '''
    Set the manager
    '''
    def set_manager(self, manager_id):
        self.manager_id = manager_id
    
    '''
    Kill a player by its id
    '''
    def kill_player(self, player_id):
        self.alive_players.remove(player_id)