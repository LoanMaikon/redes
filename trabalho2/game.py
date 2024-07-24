from src.Card import Card
from src.Deck import Deck
from src.Player import Player
from src.SocketHandler import SocketHandler
from src.RoundManager import RoundManager

import src.packets as packets

SOCKET_BUFFER_SIZE = 1024

def main():
    player_number = get_input()
    player = Player(player_number)

    sock = SocketHandler(player.get_addr1())
    sock.setTimeOut(0.1)

    estabilish_connection(sock, player)

    roundManager = RoundManager(player.get_id())

    if player.manager:
        start_queue(player, sock, roundManager)

    main_loop(player, sock, roundManager)

def main_loop(player, sock, roundManager):
    actual_packet = player.get_next_msg()
    if actual_packet:
        sock.send_packet(packets.encode_packet(actual_packet), player.get_addr2())
        player.waiting_for_response = True

    while True:
        if not player.waiting_for_response and player.baston:
            if player.msg_to_send.empty(): # Queue vazia
                if player.manager: # Nova rodada começa se for o manager
                    roundManager.next_round()
                    pass_round_manager(player, sock, roundManager)
                    switch_baston(player, sock, roundManager)
                else: # Passa o bastão
                    sock.send_packet(packets.encode_packet(packets.socket_switch_baston(player.get_id(), player.get_next_player(1))), player.get_addr2())
                    switch_baston(player, sock, roundManager)
                continue
            else: # Queue com mensagens para enviar. Envia a próxima
                actual_packet = player.get_next_msg()
                player.waiting_for_response = True
                sock.send_packet(packets.encode_packet(actual_packet), player.get_addr2())
                if actual_packet['type'] == packets.TYPE_SWITCH_BASTON
                    player.passing_baston = True
                continue

        data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)
        if not data:
            continue

        data_json = packets.decode_packet(data)

        # Se player está esperando por uma mensagem de resposta
        if player.waiting_for_response:

            # Se foi enviado pelo próprio player
            if int(data_json['src']) == player.get_id():

                # Se não foi recebido, reenvia
                if not data_json['received']:
                    sock.send_packet(data, player.get_addr2())
                    continue
                
                # Se foi recebido
                else:
                    # Se é o mesmo pacote que foi enviado pelo player destino
                    if packets.same_packet(data_json, actual_packet):
                        
                        # Se player está passando o bastão, inverte o bastão e continua
                        if player.passing_baston:
                            player.invert_baston()
                            player.waiting_for_response = False
                            continue
                        
                        else: # Senão, desenfilera a próxima mensagem
                            # Desenfilera a próxima mensagem
                            actual_packet = player.get_next_msg()

                            # Se não tem mensagem para enviar, continua
                            if not actual_packet:
                                player.waiting_for_response = False
                                continue

                            # Se o destino é o mesmo que a fonte, processa
                            if actual_packet['dest'] == player.get_id():
                                player.waiting_for_response = False
                                data_json = actual_packet

                            # Se o destino é diferente, envia e continua
                            else:
                                sock.send_packet(packets.encode_packet(actual_packet), player.get_addr2())
                                player.waiting_for_response = True
                                continue

        if int(data_json['dest']) != player.get_id():
            sock.send_packet(data, player.get_addr2())
            continue

        if int(data_json['type']) == packets.TYPE_SWITCH_BASTON:
            switch_baston(player, sock, roundManager, data_json)
        
        elif int(data_json['type']) == packets.TYPE_DISTRIBUTE_CARDS:
            distribute_cards(player, sock, roundManager, data_json)

        elif int(data_json['type']) == packets.TYPE_GUESS:
            guess(player, sock, roundManager, data_json)
        
        elif int(data_json['type']) == packets.TYPE_PLAY_CARD:
            play_card(player, sock, roundManager, data_json)

        elif int(data_json['type']) == packets.TYPE_CHANGE_MANAGER:
            change_manager(player, sock, roundManager, data_json)

        elif int(data_json['type']) == packets.TYPE_INFORM_PLAYED_CARD:
            inform_played_card(player, sock, roundManager, data_json)

        elif int(data_json['type']) == packets.TYPE_INFORM_TURNED_CARD:
            inform_turned_card(player, sock, roundManager, data_json)

        data_json['received'] = True
        sock.send_packet(packets.encode_packet(data_json), player.get_addr2())

def switch_baston(player, sock, roundManager, data_json=None):
    player.invert_baston()

def distribute_cards(player, sock, roundManager, data_json):
    player.set_cards_from_json(data_json['cards'])

    print("Cartas recebidas: ")
    print(player.get_str_cards() + '\n')

def guess(player, sock, roundManager, data_json):
    # put in the player's queue the guess and wait for the baston
    pass

def play_card(player, sock, roundManager, data_json):
    # put in the player's queue the card and wait for the baston
    #informar a carta jogada para os outros jogadores usando TYPE_INFORM_PLAYED_CARD
    pass

def change_manager(player, sock, roundManager, data_json):
    # the player who received it becomes the manager, change player.manager to True and use start_queue()
    pass

def inform_played_card(player, sock, roundManager, data_json):
    # receive a card that was played by another player and show on the screen, also send it to the next player
    # need to store who played the card and the card. stop sending when the next player is who played the card
    pass

def inform_turned_card(player, sock, roundManager, data_json):
    turned_card = Card(data_json['turned_card'][0], data_json['turned_card'][1])

    print("Carta virada: ")
    print(turned_card.get_str_card())

def start_queue(player, sock, roundManager):
    # Distributing the cards to the players
    for i in range(1, 5):
        id = player.get_next_player(i)
        player.put_msg(packets.socket_distribute_cards(player.get_id(), id, roundManager.draw_cards(id)))

    # Turning a card from the deck
    turned_card = roundManager.turn_card()

    # Informing the turned card to the players
    for i in range(1, 5):
        id = player.get_next_player(i)
        player.put_msg(packets.socket_inform_turned_card(player.get_id(), id, turned_card))

    # Asking card from the plasyers
    for i in range(1, 5):
        id = player.get_next_player(i)
        player.put_msg(packets.socket_play_card(player.get_id(), id))

    # Passing the baston
    player.put_msg(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))

def pass_round_manager(player, sock, roundManager):
    # send the roundManager to the next manager
    # send a change_manager message
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
        received = False
        while not received:
            sock.send_packet(estabilished_connetion_packet.encode(), player.get_addr2())

            data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)

            if data and data.decode() == 'conexao_estabelecida':
                sock.send_packet(init_game.encode(), player.get_addr2())

                print("Conexão estabelecida\n")
                received = True
        
        # Cleaning the buffer
        clean = False
        while not clean:
            data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)

            if data and data.decode() == 'iniciar_jogo':
                clean = True
        
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

                print("Conexão estabelecida\n")
                break

if __name__ == "__main__":
    main()
