from .Deck import Deck
from .Card import Card

class RoundManager:
    def __init__(self):
        self.deck = Deck()
        self.alive_players = [1, 2, 3, 4]
        self.players_n_cards = {i: 5 for i in self.alive_players}
        self.players_guessings = {i: None for i in self.alive_players}
        self.players_that_are_guessing = [i for i in self.alive_players]
        self.prohibited_guess = len(self.alive_players)
        self.players_cards = {}
        self.round_winner_id = None
        self.round_winner_card = None
        self.turned_card = None

    '''
    Attributes go to the next round. Deck reseted
    '''
    def next_round(self):
        self.round_winner_id = None
        self.round_winner_card = None

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
    
    '''
    Set turned card
    '''
    def set_turned_card(self, card):
        self.turned_card = card
    
    '''
    When player plays a card, remove it from his cards
    '''
    def remove_card_from_player(self, player, card):
        try:
            self.players_cards[player].remove(card)
        except:
            return
    
    '''
    Put the guess of a player in the players_guessings dict. Return 0 if player already guessed, 1 if not
    '''
    def add_player_guessing(self, player_id, guess):
        if self.players_guessings[player_id] is not None:
            return 0

        self.players_guessings[player_id] = guess
        self.players_that_are_guessing.remove(player_id)

        return 1

    '''
    Return 1 if the guess is available, 0 if not
    '''
    def validate_guessing(self, player, guessing):
        # Last player to guess
        if len(self.players_that_are_guessing) == 1 and self.players_that_are_guessing[0] == player:
            if guessing == self.prohibited_guess: # If guess is prohibited, return 0
                return 0
            
        return 1
    
    '''
    Update the round winner if card is better
    '''
    def update_round_winner(self, winner_id, card):
        if self.round_winner_card is None or self.deck.compare_cards(card, self.round_winner_card):
            self.round_winner_id = winner_id
            self.round_winner_card = card
