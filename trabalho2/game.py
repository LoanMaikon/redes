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

    roundManager = RoundManager()

    if player.manager:
        start_queue(player, sock, roundManager)

    main_loop(player, sock, roundManager)

def main_loop(player, sock, roundManager):
    while True:
        # print(f"Bastão: {player.baston}")
        # print(player.msg_to_send.queue)
        # print("Esperando resposta: ", player.waiting_for_response)
        if not player.waiting_for_response and player.baston:
            if player.msg_to_send.empty(): # Queue vazia
                # If game is over, pass the baston
                if roundManager.game_over:
                    player.put_msg(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))
                    continue

                if player.manager: # Nova rodada começa se for o manager
                    round_winner_id = roundManager.get_round_winner()
                    players_cards = roundManager.get_players_cards_to_dict()

                    transfer_manager(player, sock, roundManager, round_winner_id, players_cards)
                
                # Passando o bastão
                player.put_msg(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))

            else: # Queue com mensagens para enviar. Desenfilera a próxima
                actual_packet = player.get_next_msg()

                if actual_packet['dest'] == player.get_id():
                    execute_packet(player, sock, roundManager, actual_packet)
                    player.waiting_for_response = False
                    player.passing_baston = False
                else:
                    player.waiting_for_response = True
                    player.packet_waiting_response = actual_packet
                    sock.send_packet(packets.encode_packet(actual_packet), player.get_addr2())
                    if actual_packet['type'] == packets.TYPE_SWITCH_BASTON:
                        player.passing_baston = True

            continue

        data, _ = sock.receive_packet(SOCKET_BUFFER_SIZE)
        if not data:
            continue

        data_json = packets.decode_packet(data)

        # Se player está esperando por uma mensagem de resposta e se foi enviado pelo próprio player
        if player.waiting_for_response and int(data_json['src']) == player.get_id():

            # Se não foi recebido, reenvia
            if not data_json['received']:
                sock.send_packet(data, player.get_addr2())
                continue
            
            # Se foi recebido e é o mesmo pacote que foi enviado pelo player destino
            elif packets.same_packet(data_json, actual_packet):
    
                # Se player está passando o bastão e a mensagem é do tipo de inverter o bastão, inverte o bastão e continua
                if player.passing_baston and data_json['type'] == packets.TYPE_SWITCH_BASTON:
                    player.set_baston_to_false()
                    player.passing_baston = False

                # Se player está passando o manager e a mensagem é do tipo de passar o manager, passa o manager e continua
                elif data_json['type'] == packets.TYPE_INFORM_TO_CHANGE_MANAGER:
                    player.manager = False
                
                player.waiting_for_response = False
                continue

        if int(data_json['dest']) != player.get_id():
            sock.send_packet(data, player.get_addr2())
            continue

        execute_packet(player, sock, roundManager, data_json)

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

    elif int(data_json['type']) == packets.TYPE_START_ROUND:
        start_round(player, sock, roundManager, data_json)

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

    elif int(data_json['type']) == packets.TYPE_INFORM_TO_CHANGE_MANAGER:
        inform_to_change_manager(player, sock, roundManager, data_json)

    elif int(data_json['type']) == packets.TYPE_INFORM_ROUND_WINNER:
        inform_round_winner(player, sock, roundManager, data_json)

    elif int(data_json['type']) == packets.TYPE_INFORM_END_ROUNDS:
        inform_end_rounds(player, sock, roundManager, data_json)

    elif int(data_json['type']) == packets.TYPE_INFORM_GAME_OVER:
        inform_game_over(player, sock, roundManager, data_json)

def switch_baston(player, sock, roundManager, data_json=None):
    player.set_baston_to_true()

def distribute_cards(player, sock, roundManager, data_json):
    player.set_cards_from_json(data_json['cards'])

    print("\nCartas recebidas: ")
    print(player.get_str_cards())

def guess(player, sock, roundManager, data_json):
    validated = False
    while not validated:
        try:
            guess = int(input("\nPalpite de vitórias: "))
        except KeyboardInterrupt:
            exit(1)
        except:
            print("Número inválido. Digite novamente")
            continue

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

def play_card(player, sock, roundManager, data_json):
    played = False
    while not played:
        list_cards(player)

        try:
            card_number = int(input("\nJogue uma carta: "))
        except KeyboardInterrupt:
            exit(1)
        except:
            print("Número inválido. Digite novamente")
            continue

        try:
            card_number = int(card_number)
        except KeyboardInterrupt:
            exit(1)
        except:
            print("Número inválido. Digite novamente")
            continue

        if card_number < 1 or card_number > len(player.cards):
            print("Número inválido. Digite novamente")
            continue
        played = True

    card_played = player.play_card(card_number - 1)

    messages_to_put_first = []
    # Informing other players about the card played
    for i in range(1, 5):
        messages_to_put_first.append(packets.socket_inform_played_card(player.get_id(), player.get_next_player(i), card_played))
    # Pass the baston
    messages_to_put_first.append(packets.socket_switch_baston(player.get_id(), player.get_next_player(1)))
    player.put_msgs_first(messages_to_put_first)

def start_round(player, sock, roundManager, data_json):
    player.clear_queue()
    roundManager.next_round()

    # Asking card from the players
    for i in range(1, 5):
        if not roundManager.is_player_alive(player.get_next_player(i)) or not roundManager.player_has_cards(player.get_next_player(i)):
            continue
        player.put_msg(packets.socket_inform_player_to_play(player.get_id(), player.get_next_player(i)))

def inform_played_card(player, sock, roundManager, data_json):
    played_card = Card(data_json['played_card'][0], data_json['played_card'][1])

    if data_json['src'] != data_json['dest']:
        print(f"\nJogador {str(data_json['src'])}: ", played_card)

    roundManager.remove_card_from_player(data_json['src'], played_card)
    roundManager.update_round_winner(data_json['src'], played_card)

def inform_turned_card(player, sock, roundManager, data_json):
    turned_card = Card(data_json['turned_card'][0], data_json['turned_card'][1])

    roundManager.set_turned_card(turned_card)

    print("\nCarta virada: ")
    print(turned_card)

def inform_player_to_play(player, sock, roundManager, data_json):
    player.put_msg(packets.socket_play_card(player.get_id(), player.get_id()))

def inform_player_to_guess(player, sock, roundManager, data_json):
    player.put_msg(packets.socket_guess(player.get_id(), player.get_id()))

def inform_player_guess(player, sock, roundManager, data_json):
    if data_json['src'] != data_json['dest']:
        print(f"Jogador {str(data_json['src'])} disse que vai ganhar {str(data_json['guess'])}")

    player.add_player_guessing(data_json['src'], data_json['guess'])

    roundManager.add_player_guessing(data_json['src'], data_json['guess'])

def inform_to_change_manager(player, sock, roundManager, data_json):
    player.manager = True
    roundManager.set_players_cards_from_json(data_json['players_cards'].copy())

    if not roundManager.all_players_played(): # Start a new round
        # If the player has no cards, it passes the manager to the next player who has cards
        if not roundManager.player_has_cards(player.get_id()):
            for i in range(1, 5):
                if roundManager.player_has_cards(player.get_next_player(i)):
                    player.put_msg(packets.socket_inform_to_change_manager(player.get_id(), player.get_next_player(1),
                                                                           roundManager.get_players_cards_to_dict()))
                    return

        player.put_msg(packets.socket_start_round(player.get_id(), player.get_id()))

    else: # Start a new series of rounds
        roundManager.recalculate_lives()

        for i in range(1, 5):
            player.put_msg(packets.socket_inform_end_rounds(player.get_id(), player.get_next_player(i)))

        # If there is only one player alive, the game is over
        if roundManager.is_over():
            msgs_to_put_first = []
            for i in range(1, 5):
                msgs_to_put_first.append(packets.socket_inform_game_over(player.get_id(), player.get_next_player(i), roundManager.get_last_alive_player()))
            player.put_msgs_first(msgs_to_put_first)
            return

        # If the player is dead, it passes the manager to the next player alive
        if not roundManager.is_player_alive(player.get_id()):
            for i in range(1, 5):
                if roundManager.is_player_alive(player.get_next_player(i)):
                    player.put_msg(packets.socket_inform_to_change_manager(player.get_id(), player.get_next_player(i), roundManager.get_players_cards_to_dict()))
                    return
            
            # if no player is alive, the game is over
            msgs_to_put_first = []
            for i in range(1, 5):
                msgs_to_put_first.append(packets.socket_inform_game_over(player.get_id(), player.get_next_player(i), None))
            player.put_msgs_first(msgs_to_put_first)
            return
        
        roundManager.clear()
        player.clear(roundManager.get_alive_players())

        start_queue(player, sock, roundManager)

def inform_round_winner(player, sock, roundManager, data_json):
    print(f"Jogador {str(data_json['winner'])} ganhou a rodada")

    roundManager.add_win_to_player(data_json['winner'])

def inform_end_rounds(player, sock, roundManager, data_json):
    if not player.manager:
        roundManager.recalculate_lives()
        roundManager.clear()

        player.clear(roundManager.get_alive_players())

    players_lives = roundManager.get_players_lives()

    print("\nFim da rodada")
    print("\nPlacar: ")
    for i in range(1, 5):
        print(f"Jogador {str(i)}: {players_lives[str(i)]} vidas")

def inform_game_over(player, sock, roundManager, data_json):
    if data_json['winner_id'] is None:
        print("\nNinguém ganhou o jogo")
    else:
        print(f"\nJogador {str(data_json['winner_id'])} ganhou o jogo")

    player.clear_queue()
    roundManager.game_over = True

def start_queue(player, sock, roundManager):
    # Distributing the cards to the players
    for i in range(1, 5):
        id = player.get_next_player(i)
        if not roundManager.is_player_alive(id):
            continue
        player.put_msg(packets.socket_distribute_cards(player.get_id(), id, roundManager.draw_cards(id)))

    # Turning a card from the deck
    turned_card = roundManager.turn_card()

    # Informing the turned card to the players
    for i in range(1, 5):
        player.put_msg(packets.socket_inform_turned_card(player.get_id(), player.get_next_player(i), turned_card))

    # Asking guessings from the players
    for i in range(1, 5):
        if not roundManager.is_player_alive(player.get_next_player(i)):
            continue
        player.put_msg(packets.socket_inform_player_to_guess(player.get_id(), player.get_next_player(i)))

    # Asking card from the players
    for i in range(1, 5):
        if not roundManager.is_player_alive(player.get_next_player(i)):
            continue
        player.put_msg(packets.socket_inform_player_to_play(player.get_id(), player.get_next_player(i)))

def transfer_manager(player, sock, roundManager, round_winner_id, players_cards):
    for i in range(1, 5):
        player.put_msg(packets.socket_inform_round_winner(player.get_id(), player.get_next_player(i), round_winner_id))

    if not roundManager.is_over():
        player.put_msg(packets.socket_inform_to_change_manager(player.get_id(), round_winner_id, players_cards))
    else: # Game is over
        for i in range(1, 5):
            player.put_msgs_first([packets.socket_inform_game_over(player.get_id(), player.get_next_player(i), roundManager.get_last_alive_player())])

def list_cards(player):
    print("\nSuas cartas: ")
    for i, card in enumerate(player.cards):
        print(str(i + 1) + ". " + str(card))

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
