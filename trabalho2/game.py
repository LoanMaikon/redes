from src.Card import Card
from src.Deck import Deck
from src.Player import Player
from src.SocketHandler import SocketHandler
from src.RoundManager import RoundManager

import src.packets as packets

import socket

SOCKET_BUFFER_SIZE = 1024

def main():
    player_number = get_input()
    player = Player(player_number)

    sock = SocketHandler(player.get_addr1())
    sock.setTimeOut(0.1)

    estabilish_connection(sock, player)

    roundManager = RoundManager()

    main_loop(player, sock, roundManager)

def main_loop(player, sock, roundManager):
    while True:
        if player.baston and player.manager and player.msg_to_send.empty():
            roundManager.next_round()
            pass_round_manager(player, sock, roundManager)
            pass_baston(player, sock, roundManager)
            continue

        data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)
        if not data:
            continue

        data_json = data.decode()

        if data_json['dest'] != player.get_id():
            sock.send_packet(data, player.get_addr2())
            continue

        if data_json['type'] == packets.TYPE_PASS_BASTON:
            pass_baston(player, sock, roundManager)
        
        elif data_json['type'] == packets.TYPE_DISTRIBUTE_CARDS:
            distribute_cards(player, sock, roundManager)

        elif data_json['type'] == packets.TYPE_GUESS:
            guess(player, sock, roundManager)
        
        elif data_json['type'] == packets.TYPE_PLAY_CARD:
            play_card(player, sock, roundManager)

        elif data_json['type'] == packets.TYPE_CHANGE_MANAGER:
            change_manager(player, sock, roundManager)

def pass_baston(player, sock, roundManager):
    # use player.get_next_player()
    pass

def distribute_cards(player, sock, roundManager):
    pass

def guess(player, sock, roundManager):
    pass

def play_card(player, sock, roundManager):
    pass

def pass_round_manager(player, sock, roundManager):
    # copy the roundManager to the next manager
    # add things to the queue of the new manager
    pass

def change_manager(player, sock, roundManager):
    # change the manager to the next player
    pass

def get_input():
    print("Digite o player que deseja ser: ")
    print("1 - Player 1")
    print("2 - Player 2")
    print("3 - Player 3")
    print("4 - Player 4")
    player_number = int(input())

    return player_number

def estabilish_connection(sock, player):
    estabilished_connetion_packet = 'conexao_estabelecida' # Fazer um packet depois
    init_game = 'iniciar_jogo' # Fazer um packet depois

    if player.get_id() == 1:
        recebeu = False
        while not recebeu:
            sock.send_packet(estabilished_connetion_packet.encode(), player.get_addr2())

            data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)

            if data and data.decode() == 'conexao_estabelecida':
                sock.send_packet(init_game.encode(), player.get_addr2())

                print("Conexão estabelecida")
                recebeu = True
        
    else:
        while True:
            data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)
            if data and data.decode() == 'conexao_estabelecida':
                break
        
        while True:
            sock.send_packet(estabilished_connetion_packet.encode(), player.get_addr2())

            data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)

            if data and data.decode() == 'iniciar_jogo':
                sock.send_packet(init_game.encode(), player.get_addr2())

                print("Conexão estabelecida")
                break

if __name__ == "__main__":
    main()
