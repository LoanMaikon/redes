from .Card import Card

import json

TYPE_SWITCH_BASTON = 1
TYPE_DISTRIBUTE_CARDS = 2
TYPE_GUESS = 3
TYPE_PLAY_CARD = 4
TYPE_CHANGE_MANAGER = 5
TYPE_INFORM_PLAYED_CARD = 6
TYPE_INFORM_TURNED_CARD = 7
TYPE_INFORM_PLAYER_TO_PLAY = 8

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

def socket_guess():
    pass

def socket_play_card(src, dest):
    packet = {
        'type': TYPE_PLAY_CARD,
        'src': src,
        'dest': dest,
        'received': False
    }

    return packet

def socket_change_manager():
    pass

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
