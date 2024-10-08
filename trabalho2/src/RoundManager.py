from .Deck import Deck
from .Card import Card

class RoundManager:
    def __init__(self):
        self.deck = Deck()
        self.alive_players = [1, 2, 3, 4]
        self.players_n_cards = {str(i): 5 for i in self.alive_players}
        self.players_guessings = {str(i): None for i in self.alive_players}
        self.players_wins = {str(i): 0 for i in self.alive_players}
        self.players_that_are_guessing = [i for i in self.alive_players]
        self.players_lives = {str(i): 5 for i in self.alive_players}
        self.prohibited_guess = len(self.alive_players)
        self.players_cards = {str(i): None for i in self.alive_players}
        self.round_winner_id = None
        self.round_winner_card = None
        self.turned_card = None
        self.recalculated_lives = False
        self.game_over = False

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
        cards = self.deck.draw_cards(self.players_n_cards[str(player_id)])
        self.players_cards[str(player_id)] = cards

        return cards
    
    '''
    Return the players_cards
    '''
    def get_players_cards_to_dict(self):
        players_cards_new = {}
        for player in self.players_cards:
            players_cards_new[str(player)] = [card.to_list() for card in self.players_cards[player]]

        return players_cards_new
    
    '''
    Return a list of alive players
    '''
    def get_alive_players(self):
        return self.alive_players
    
    '''
    Return the players lives
    '''
    def get_players_lives(self):
        return self.players_lives
    
    '''
    Set the players_cards
    '''
    def set_players_cards_from_json(self, players_cards):
        self.players_cards = {}
        for player in players_cards:
            self.players_cards[str(player)] = [Card(card[0], card[1]) for card in players_cards[player]]
    
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
        self.deck.order_power_by_shackle(card)

    '''
    Return the turned card
    '''
    def get_turned_card(self):
        return self.turned_card
    
    '''
    When player plays a card, remove it from his cards
    '''
    def remove_card_from_player(self, player, card):
        try:
            for p_card in self.players_cards[str(player)]:
                if p_card.get_value() == card.get_value() and p_card.get_suit() == card.get_suit():
                    self.players_cards[str(player)].remove(p_card)
                    return

        except:
            return
    
    '''
    Put the guess of a player in the players_guessings dict. Return 0 if player already guessed, 1 if not
    '''
    def add_player_guessing(self, player_id, guess):
        if self.players_guessings[str(player_id)] is not None:
            return 0

        self.players_guessings[str(player_id)] = guess
        self.players_that_are_guessing.remove(player_id)

        return 1
    
    '''
    Return the players wins
    '''
    def get_players_wins(self):
        return self.players_wins

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

    '''
    Add a win to a player
    '''
    def add_win_to_player(self, player_id):
        self.players_wins[str(player_id)] += 1

        self.recalculated_lives = False

    '''
    Get the round winner
    '''
    def get_round_winner(self):
        return int(self.round_winner_id)

    '''
    Return 1 if all the players played all their cards, 0 if not
    '''
    def all_players_played(self):
        for player in self.alive_players:
            if len(self.players_cards[str(player)]) > 0:
                return 0
        return 1
    
    '''
    Return 1 if the player is alive
    '''
    def is_player_alive(self, player_id):
        if player_id in self.alive_players:
            return 1
        return 0
    
    '''
    Print the lost lives of the players
    '''
    def print_lives(self):
        for player in self.alive_players:
            print(f'Player {player} has {self.players_lives[str(player)]} lives')

    '''
    Recalculate lives of the players
    '''
    def recalculate_lives(self):
        if self.recalculated_lives:
            return

        for player in range(1, 5):
            if player not in self.alive_players:
                continue

            diff = abs(self.players_guessings[str(player)] - self.players_wins[str(player)])

            self.players_lives[str(player)] -= diff

            if self.players_lives[str(player)] <= 0:
                self.players_lives[str(player)] = 0
                self.kill_player(player)
        
        self.recalculated_lives = True

    '''
    Clear informations. Observation: it doesn't reset the deck
    '''
    def clear(self):
        self.players_n_cards = {str(i): self.players_lives[str(i)] for i in self.alive_players}
        self.players_guessings = {str(i): None for i in self.alive_players}
        self.players_wins = {str(i): 0 for i in self.alive_players}
        self.players_that_are_guessing = [i for i in self.alive_players]
        self.players_cards = {}
        self.round_winner_id = None
        self.round_winner_card = None
        self.turned_card = None
        self.prohibited_guess = len(self.alive_players)
        self.deck.reset_deck()

    '''
    Return the number of wins of a player
    '''
    def get_player_wins(self, player_id):
        return self.players_wins[str(player_id)]
    
    '''
    Reset the deck
    '''
    def reset_deck(self):
        self.deck.reset_deck()

    '''
    Return True if there's only one player alive
    '''
    def is_over(self):
        if len(self.alive_players) == 1:
            return True
        return False

    '''
    Get last alive player
    '''
    def get_last_alive_player(self):
        if len(self.alive_players) > 1 or len(self.alive_players) == 0:
            return None
        return self.alive_players[0]

    '''
    Return True if a player still have cards
    '''
    def player_has_cards(self, player_id):
        if str(player_id) not in self.players_cards:
            return False

        if len(self.players_cards[str(player_id)]) > 0:
            return True
        return False
