#include "../header/client_tools.h"

unsigned int get_user_input(char *text) {
    char option[64];
    unsigned int option_int = 0;

    while (1) {
        printf("%s", text);
        fgets(option, sizeof(option), stdin);

        option[strcspn(option, "\n")] = '\0';
        option_int = atoi(option);

        if (option_int) {
            return option_int;
        }
        printf("Opcao invalida\n");
    }
}

void print_movie(unsigned char *packet, unsigned int id_movie) {
    unsigned char *data = packet + 3;

    if (id_movie % 2 == 0) {
        printf("%d- %-30s\n", id_movie, data);
    }
    else {
        printf("%d- %-30s ", id_movie, data);
    }
}

int recv_and_print_movie_names_packets(int sockfd, unsigned char *packet_server) {
    unsigned char code = 0;
    unsigned char seq = 0, last_seq = 0;
    unsigned int success = 1, id_movie = 1;

    printf("\n-Filmes-------------------------------------\n");
    while (1) {
        if (!recv_packet_in_timeout(sockfd, packet_server)) {
            success = 0;
            break;
        }
        code = get_packet_code(packet_server);
        if ((code != SHOW_IN_SCREEN_COD) && (code != END_DATA_COD)) {
            send_NACK(sockfd, 0);
            continue;
        }
        seq = get_packet_seq(packet_server);
        if (seq == (last_seq + 1) || (id_movie == 1)) {
            last_seq = seq;
            print_movie(packet_server, id_movie);
            id_movie++;
            send_ACK(sockfd, seq);
        }
        else if (seq == last_seq) {
            send_ACK(sockfd, seq);
        }
        if (code == END_DATA_COD) {
            break;
        }
    }
    printf("\n--------------------------------------------\n");

    return success;
}

int view_movies_list(int sockfd, unsigned char *packet_server) {
    unsigned char *solicit_movies_pckt = create_packet(NULL, 0, 0, LIST_FILES_COD);

    if (!send_packet_with_confirm(sockfd, solicit_movies_pckt, packet_server)) {
        free(solicit_movies_pckt);
        return 0;
    }
    free(solicit_movies_pckt);

    return recv_and_print_movie_names_packets(sockfd, packet_server);
}

int recv_file(int sockfd, char *filename) {
    FILE *file = fopen(filename, "wb");
    if (file == NULL) {
        fprintf(stderr, "Erro ao abrir o arquivo\n");
        return 0;
    }

    unsigned char buffer[PACKET_SIZE] = {0};
    short n = 0;
    unsigned char last_seq = -1, seq = 0, cod = 0;
    unsigned long int num_packets = 0;
    unsigned short tam_data = 0;

    while (1) {
        n = recv(sockfd, buffer, PACKET_SIZE, 0);

        if (n == -1) {
            continue;
        }

        n = validate_packet(buffer, n);
        if (!n) {
            send_NACK(sockfd, seq);
            continue;
        }

        seq = get_packet_seq(buffer);
        cod = get_packet_code(buffer);

        if ((cod != DATA_COD) && (cod != END_DATA_COD)) {
            send_NACK(sockfd, seq);
            continue;
        }

        if (seq == last_seq) {
            send_ACK(sockfd, seq);
            continue;
        }
        last_seq = seq;

        send_ACK(sockfd, seq);

        tam_data = get_packet_data_size(buffer);

        fwrite(buffer + 3, 1, tam_data, file);
        num_packets++;

        if (cod == END_DATA_COD) {
            break;
        }
    }
    printf("Recebidos %ld pacotes\n", num_packets);

    return 1;
}
