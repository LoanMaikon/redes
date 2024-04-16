#include "socket.h"

int create_socket() {
    int socket_fd;
    struct sockaddr_ll socket_address;
    struct ifreq ifr;

    socket_fd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (socket_fd < 0) {
        perror("Erro ao criar socket\n");
        return -1;
    }

    memset(&socket_address, 0, sizeof(socket_address));
    socket_address.sll_family = AF_PACKET;
    socket_address.sll_protocol = htons(ETH_P_ALL);
    socket_address.sll_ifindex = ifr.ifr_ifindex;

    if (bind(socket_fd, (struct sockaddr *)&socket_address, sizeof(socket_address)) < 0) {
        perror("Erro ao fazer bind\n");
        return -1;
    }

    return socket_fd;
}