#include "../header/basic_for_packets.h"
#include <stdio.h>

unsigned char calc_crc_8(const unsigned char *data, const short size) {
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
short validate_crc_8(const unsigned char *data, const short size) {
    unsigned char crc = calc_crc_8(data + 1, size-2);
    return crc == data[size-1];
}

/* Retorna 1 se for valido e 0 se nao for. */
short validate_packet(const unsigned char *data, const short size) {
    if ((size < PACKET_SIZE) || (data[0] != 0x7e)) {
        return 0;
    }

    if (validate_crc_8(data, size)) {
        return 1;
    }
    return 0;
}

unsigned char **segment_data_in_packets(unsigned char *data, 
                                        const unsigned long int size) {
    if (size == 0) {
        return NULL;
    }

    unsigned short max_size_data = PACKET_SIZE - 4;
    unsigned long int num_packets = size / max_size_data;
    unsigned short last_packet_size = size % max_size_data;

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
        packets[i] = calloc(PACKET_SIZE, sizeof(unsigned char));
        packets[i][0] = INIT_MARKER;
        packets[i][1] = (max_size_data << 2) | (sequence >> 3);
        packets[i][2] = (sequence << 5) | DATA_COD;
        memcpy(packets[i] + 3, data, max_size_data);
        data += max_size_data;
        ++sequence;
        sequence &= 0x1f;
        packets[i][PACKET_SIZE - 1] = calc_crc_8(packets[i] + 1, PACKET_SIZE - 2);
    }
    packets[i] = calloc(PACKET_SIZE, sizeof(unsigned char));
    packets[i][0] = INIT_MARKER;
    packets[i][1] = ((last_packet_size << 2) | (sequence >> 3));
    packets[i][2] = (sequence << 5) | END_DATA_COD;
    memcpy(packets[i] + 3, data, last_packet_size);
    packets[i][PACKET_SIZE - 1] = calc_crc_8(packets[i] + 1, PACKET_SIZE - 2);

    packets[num_packets] = NULL;

    return packets;
}

void free_packets(unsigned char ***packets) {
    for (unsigned long int i = 0; (*packets)[i] != NULL; i++) {
        free((*packets)[i]);
    }
    free(*packets);
}

void clear_socket_buffer(int sockfd) {
    unsigned char buffer[PACKET_SIZE] = {0};
    while (recv(sockfd, buffer, PACKET_SIZE, MSG_DONTWAIT) != -1);
}
