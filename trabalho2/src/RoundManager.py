from .Deck import Deck
from .Card import Card

class RoundManager:
    def __init__(self, manager_id):
        self.deck = Deck()
        self.manager_id = manager_id
        self.alive_players = [1, 2, 3, 4]
        self.players_n_cards = {i: 5 for i in self.alive_players}
        self.players_cards = {}
        self.round = 1
        self.turned_card = None

    '''
    Attributes go to the next round. Deck reseted
    '''
    def next_round(self):
        self.deck.reset_deck()
        self.round += 1
        self.turned_card = None
        self.players_cards = {}

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

    '''
    Draw n cards from the deck and attribute to a player. Return the cards drawed
    '''
    def draw_cards(self, player_id):
        cards = self.deck.draw_cards(self.players_n_cards[player_id])
        self.players_cards[player_id] = cards

        return cards
    
    '''
    Turns a card from the deck and return it
    '''
    def turn_card(self):
        self.turned_card = self.deck.turn_card()

        return self.turned_card
    
    