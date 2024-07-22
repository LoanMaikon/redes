from src.Card import Card
from src.Deck import Deck
from src.Player import Player
from src.SocketHandler import SocketHandler

import socket

SOCKET_BUFFER_SIZE = 1024

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

def create_deck(player_id):
    deck = None
    if player_id == 1:
        deck = Deck()
    
    return deck

def distribute_cards(deck, player, sock):
    pass

def main():
    player_number = get_input()
    player = Player(player_number)

    sock = SocketHandler(player.get_addr1())
    sock.setTimeOut(0.1)

    estabilish_connection(sock, player)

    deck = create_deck(player.get_id())
    distribute_cards(deck, player, sock)

if __name__ == "__main__":
    main()
