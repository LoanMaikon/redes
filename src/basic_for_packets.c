#include "../header/basic_for_packets.h"
#include <stdio.h>


unsigned char calc_crc_8(unsigned char *data, const short size) {
    unsigned char crc = 0;
    for (int i = 0; i < size; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 0x80) {
                crc = (crc << 1) ^ CRC_8_POLY;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc;
}

/* Retorna 1 se for valido e 0 se nao for. */
short validate_crc_8(unsigned char *data, const short size) {
    unsigned char crc = calc_crc_8(data + 1, size-2);
    return crc == data[size-1];
}

/* Retorna o tamanho real do pacote se for valido e 0 se nao for. */
short validate_packet(unsigned char *data, const short size) {
    if ((size < PACKET_MIN_SIZE) || (data[0] != 0x7e)) {
        printf("Size: %d   ou data != \n", size);
        return 0;
    }
    short tam_packet = 0;
    tam_packet = data[1] >> 2;
    tam_packet += 4;

    if (validate_crc_8(data, tam_packet)) {
        return tam_packet;
    }
    printf("CRC error\n");
    return 0;
}

unsigned char **segment_data_in_packets(unsigned char *data, 
                                        const unsigned long int size) {
    if (size == 0) {
        return NULL;
    }

    unsigned long int num_packets = size / PACKET_MAX_SIZE;
    unsigned short last_packet_size = size % PACKET_MAX_SIZE;
    unsigned short max_size_data = PACKET_MAX_SIZE - 4;

    if (last_packet_size != 0) {
        ++num_packets;
    } 
    else {
        last_packet_size = max_size_data;
    }

    unsigned char **packets = malloc(sizeof(unsigned char *) * (num_packets + 1));
    unsigned char sequence = 0;
    unsigned long int i = 0;

    for (; i < num_packets - 1; i++) {
        packets[i] = malloc(sizeof(unsigned char) * PACKET_MAX_SIZE);
        packets[i][0] = 0x7e;
        packets[i][1] = (max_size_data << 2) | (sequence >> 3);
        packets[i][2] = (sequence << 5) | DATA_COD;
        memcpy(packets[i] + 3, data, max_size_data);
        data += max_size_data;
        ++sequence;
        packets[i][PACKET_MAX_SIZE - 1] = calc_crc_8(packets[i] + 1, PACKET_MAX_SIZE - 2);
    }
    packets[i] = malloc(sizeof(unsigned char) * (last_packet_size + 4));
    packets[i][0] = 0x7e;
    packets[i][1] = ((last_packet_size << 2) | (sequence >> 3));
    packets[i][2] = (sequence << 5) | END_DATA_COD;
    memcpy(packets[i] + 3, data, last_packet_size);
    packets[i][last_packet_size + 3] = calc_crc_8(packets[i] + 1, last_packet_size + 2);

    packets[num_packets] = NULL;

    return packets;
}

void free_packets(unsigned char ***packets) {
    for (unsigned long int i = 0; (*packets)[i] != NULL; i++) {
        free((*packets)[i]);
    }
    free(*packets);
}

short send_packet(int sockfd, unsigned char *packet) {
    short tam_packet = packet[1] >> 2;
    tam_packet += 4;
    return send(sockfd, packet, tam_packet, 0);
}

