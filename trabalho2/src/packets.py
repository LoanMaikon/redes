from .Card import Card

import json

TYPE_SWITCH_BASTON = 1
TYPE_DISTRIBUTE_CARDS = 2
TYPE_GUESS = 3
TYPE_PLAY_CARD = 4
TYPE_START_ROUND = 5
TYPE_INFORM_PLAYED_CARD = 6
TYPE_INFORM_TURNED_CARD = 7
TYPE_INFORM_PLAYER_TO_PLAY = 8
TYPE_INFORM_PLAYER_TO_GUESS = 9
TYPE_INFORM_PLAYER_GUESS = 10
TYPE_INFORM_TO_CHANGE_MANAGER = 11
TYPE_INFORM_ROUND_WINNER = 12
TYPE_INFORM_END_ROUNDS = 13
TYPE_INFORM_MANAGER_TO_TURN_CARD = 14
TYPE_INFORM_GAME_OVER = 15

def socket_switch_baston(src, dest):
    packet = {
        'type': TYPE_SWITCH_BASTON,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_distribute_cards(src, dest, cards):
    packet = {
        'type': TYPE_DISTRIBUTE_CARDS,
        'src': src,
        'dest': dest,
        'cards': [card.to_list() for card in cards],
        'received': False
    }

    return packet

def socket_guess(src, dest):
    packet = {
        'type': TYPE_GUESS,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_play_card(src, dest):
    packet = {
        'type': TYPE_PLAY_CARD,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_start_round(src, dest):
    packet = {
        'type': TYPE_START_ROUND,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_inform_played_card(src, dest, played_card):
    packet = {
        'type': TYPE_INFORM_PLAYED_CARD,
        'src': src,
        'dest': dest,
        'played_card': played_card.to_list(),
        'received': False
    }

    return packet

def socket_inform_turned_card(src, dest, turned_card):
    packet = {
        'type': TYPE_INFORM_TURNED_CARD,
        'src': src,
        'dest': dest,
        'turned_card': turned_card.to_list(),
        'received': False
    }

    return packet

def socket_inform_player_to_play(src, dest):
    packet = {
        'type': TYPE_INFORM_PLAYER_TO_PLAY,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_inform_player_to_guess(src, dest):
    packet = {
        'type': TYPE_INFORM_PLAYER_TO_GUESS,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_inform_player_guess(src, dest, guess):
    packet = {
        'type': TYPE_INFORM_PLAYER_GUESS,
        'src': src,
        'dest': dest,
        'guess': guess,
        'received': False
    }

    return packet

def socket_inform_to_change_manager(src, dest, players_cards):
    packet = {
        'type': TYPE_INFORM_TO_CHANGE_MANAGER,
        'src': src,
        'dest': dest,
        'players_cards': players_cards,
        'received': False
    }

    return packet

def socket_inform_round_winner(src, dest, winner):
    packet = {
        'type': TYPE_INFORM_ROUND_WINNER,
        'src': src,
        'dest': dest,
        'winner': winner,
        'received': False
    }

    return packet

def socket_inform_end_rounds(src, dest):
    packet = {
        'type': TYPE_INFORM_END_ROUNDS,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_inform_manager_to_turn_card(src, dest):
    packet = {
        'type': TYPE_INFORM_MANAGER_TO_TURN_CARD,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_inform_game_over(src, dest, winner_id):
    packet = {
        'type': TYPE_INFORM_GAME_OVER,
        'src': src,
        'dest': dest,
        'winner_id': winner_id,
        'received': False
    }

    return packet

def same_packet(packet1, packet2):
    keys1 = packet1.keys()
    keys2 = packet2.keys()

    for key in keys1:
        if key == 'received':
            continue

        if not key in keys2 or packet1[key] != packet2[key]:
            return False
    
    return True

def encode_packet(packet):
    return json.dumps(packet).encode()

def decode_packet(packet):
    return json.loads(packet.decode('utf-8'))
