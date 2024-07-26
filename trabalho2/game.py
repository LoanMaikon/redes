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
        print(f"Bastão: {player.baston}")
        print(player.msg_to_send.queue)
        print("Esperando resposta: ", player.waiting_for_response)
        if not player.waiting_for_response and player.baston:
            if player.msg_to_send.empty(): # Queue vazia
                if player.manager: # Nova rodada começa se for o manager
                    roundManager.next_round()
                    pass_round_manager(player, sock, roundManager)
                    
                # Passa o bastão
                player.waiting_for_response = True
                sock.send_packet(packets.encode_packet(packets.socket_switch_baston(player.get_id(), player.get_next_player(1))), player.get_addr2())
                player.passing_baston = True

                continue
            else: # Queue com mensagens para enviar. Desenfilera a próxima
                actual_packet = player.get_next_msg()

                if actual_packet['dest'] == player.get_id():
                    execute_packet(player, sock, roundManager, actual_packet)
                    player.waiting_for_response = False
                    player.passing_baston = False
                else:
                    player.waiting_for_response = True
                    sock.send_packet(packets.encode_packet(actual_packet), player.get_addr2())
                    if actual_packet['type'] == packets.TYPE_SWITCH_BASTON:
                        player.passing_baston = True
                continue

        data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)
        if not data:
            continue

        data_json = packets.decode_packet(data)

        message_from_player_itself = False

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
           
                        # Se player está passando o bastão e a mensagem é do tipo de inverter o bastão, inverte o bastão e continua
                        if player.passing_baston and data_json['type'] == packets.TYPE_SWITCH_BASTON:
                            player.set_baston_to_false()
                            player.waiting_for_response = False
                            player.passing_baston = False
                            continue
                        
                        else: # Senão
                            # Desenfilera a próxima mensagem
                            actual_packet = player.get_next_msg()

                            # Se não tem mensagem para enviar, continua
                            if not actual_packet:
                                player.waiting_for_response = False
                                continue

                            # Se o destino é o mesmo que a fonte, processa
                            if actual_packet['dest'] == actual_packet['src']:
                                player.waiting_for_response = False
                                message_from_player_itself = True
                                data_json = actual_packet

                            # Se o destino é diferente, envia e continua
                            else:
                                sock.send_packet(packets.encode_packet(actual_packet), player.get_addr2())
                                player.waiting_for_response = True
                                continue

        if int(data_json['dest']) != player.get_id():
            sock.send_packet(data, player.get_addr2())
            continue

        execute_packet(player, sock, roundManager, data_json)

        # Se não for o próprio player que enviou uma mensagem para si mesmo, passa a mensagem de resposta
        if not message_from_player_itself:
            data_json['received'] = True
            sock.send_packet(packets.encode_packet(data_json), player.get_addr2())

def execute_packet(player, sock, roundManager, data_json):
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

    elif int(data_json['type']) == packets.TYPE_INFORM_PLAYER_TO_PLAY:
        inform_player_to_play(player, sock, roundManager, data_json)

    elif int(data_json['type']) == packets.TYPE_INFORM_PLAYER_TO_GUESS:
        inform_player_to_guess(player, sock, roundManager, data_json)

    elif int(data_json['type']) == packets.TYPE_INFORM_PLAYER_GUESS:
        inform_player_guess(player, sock, roundManager, data_json)

    elif int(data_json['type']) == packets.TYPE_INFORM_MANAGER_ID:
        inform_player_manager_id(player, sock, roundManager, data_json)

def switch_baston(player, sock, roundManager, data_json=None):
    player.set_baston_to_true()

def distribute_cards(player, sock, roundManager, data_json):
    player.set_cards_from_json(data_json['cards'])

    print("Cartas recebidas: ")
    print(player.get_str_cards())

def guess(player, sock, roundManager, data_json):
    validated = False
    while not validated:
        guess = int(input("Digite o número de rodadas que você acha que vai ganhar: "))
        if player.validate_guess(guess):
            validated = True
        else:
            print("Esse número não está disponível")
    
    # Informing other player's about the guess
    messages_to_put_first = []
    for i in range(1, 5):
        messages_to_put_first.append(packets.socket_inform_player_guess(player.get_id(), player.get_next_player(i), guess))
    # Passing the baston
    messages_to_put_first.append(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))
    player.put_msgs_first(messages_to_put_first)

    print("queue depois de adivinhar")
    print(player.msg_to_send.queue)

def play_card(player, sock, roundManager, data_json):
    played = False
    while not played:
        list_cards(player)
        card_number = int(input("Digite o número da carta que deseja jogar: "))
        if card_number < 1 or card_number > len(player.cards):
            print("Número inválido. Digite novamente")
            continue
        played = True

    card_played = player.play_card(card_number - 1)

    messages_to_put_first = []
    # Informing other players about the card played
    for i in range(1, 5): # 1 until 3 because the player itself is already informed
        messages_to_put_first.append(packets.socket_inform_played_card(player.get_id(), player.get_next_player(i), card_played))
    # Pass the baston
    messages_to_put_first.append(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))
    player.put_msgs_first(messages_to_put_first)


    print("queue depois de jogar")
    print(player.msg_to_send.queue)

def change_manager(player, sock, roundManager, data_json):
    # the player who received it becomes the manager, change player.manager to True and use start_queue()
    pass

def inform_played_card(player, sock, roundManager, data_json):
    played_card = Card(data_json['played_card'][0], data_json['played_card'][1])

    print(f"Carta jogada por Jogador {str(data_json['src'])}: ", played_card.get_str_card())

    if player.manager:
        roundManager.remove_card_from_player(data_json['src'], played_card)

def inform_turned_card(player, sock, roundManager, data_json):
    turned_card = Card(data_json['turned_card'][0], data_json['turned_card'][1])

    print("Carta virada: ")
    print(turned_card.get_str_card())

def inform_player_to_play(player, sock, roundManager, data_json):
    player.put_msg(packets.socket_play_card(player.get_id(), player.get_id()))

def inform_player_to_guess(player, sock, roundManager, data_json):
    player.put_msg(packets.socket_guess(player.get_id(), player.get_id()))

def inform_player_guess(player, sock, roundManager, data_json):
    print(f"Jogador {str(data_json['src'])} disse que vai ganhar {str(data_json['guess'])}")

    player.add_player_guessing(data_json['src'], data_json['guess'])

def inform_player_manager_id(player, sock, roundManager, data_json):
    player.set_manager_id(data_json['manager_id'])

def start_queue(player, sock, roundManager):
    # Informing the manager id to the players
    for i in range(1, 5):
        player.put_msg(packets.socket_inform_manager_id(player.get_id(), player.get_next_player(i), player.get_id()))

    # Distributing the cards to the players
    for i in range(1, 5):
        id = player.get_next_player(i)
        player.put_msg(packets.socket_distribute_cards(player.get_id(), id, roundManager.draw_cards(id)))

    # Turning a card from the deck
    turned_card = roundManager.turn_card()

    # Informing the turned card to the players
    for i in range(1, 5):
        player.put_msg(packets.socket_inform_turned_card(player.get_id(), player.get_next_player(i), turned_card))

    # Asking guessings from the players
    for i in range(1, 5):
        player.put_msg(packets.socket_inform_player_to_guess(player.get_id(), player.get_next_player(i)))

    # Passing the baston
    player.put_msg(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))

    # Asking card from the players
    for i in range(1, 5):
        player.put_msg(packets.socket_inform_player_to_play(player.get_id(), player.get_next_player(i)))

    # Passing the baston
    player.put_msg(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))


    print("queue antes de tudo")
    print(player.msg_to_send.queue)

def pass_round_manager(player, sock, roundManager):
    # send the roundManager to the next manager
    # send a change_manager message
    pass

def list_cards(player):
    print("Suas cartas: ")
    for i, card in enumerate(player.cards):
        print(str(i + 1) + ". " + card.get_str_card())

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
