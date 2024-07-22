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
    init_packet = 'conexao_estabelecida'.encode() # Fazer um packet depois

    if player.get_id() == 1:
        recebeu = False
        while not recebeu:
            #sock.send_packet(init_packet, player.get_addr2())
            sock.sock.sendto(init_packet, player.get_addr2())

            #data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)
            try:
                data, _ = sock.sock.recvfrom(SOCKET_BUFFER_SIZE)
            except:
                continue

            if data:
                print("Conexão estabelecida")
                recebeu = True
        
    else:
        while True:
            #data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)
            try:
                data, _ = sock.sock.recvfrom(SOCKET_BUFFER_SIZE)
            except:
                continue
            if data:
                break
        
        while True:
            #sock.send_packet(init_packet, player.get_addr2())
            sock.sock.sendto(init_packet, player.get_addr2())


    #     recebeu = False
    #     while not recebeu:
    #         sock.sendto(msg.encode(), addr2)

    #         data, addr = sock.recvfrom(1024)
            
    #         if data:
    #             print("Mensagem recebida: ", data.decode())
    #             recebeu = True
        
    # else:
    #     while True:
    #         data, addr = sock.recvfrom(1024)
    #         if data:
    #             print("Mensagem recebida: ", data.decode())
    #             break
        
    #     while True:
    #         sock.sendto(data, addr2)

def main():
    player_number = get_input()
    player = Player(player_number)

    sock = SocketHandler()
    sock.setTimeOut(0.1)

    estabilish_connection(sock, player)

if __name__ == "__main__":
    main()
