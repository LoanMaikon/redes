#include "socket.h"

int create_socket(char *interface_name) {
    int socket_fd;
    struct sockaddr_ll socket_address;
    struct ifreq ifr;
    struct packet_mreq mr;

    socket_fd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (socket_fd < 0) {
        perror("Erro ao criar socket\n");
        return -1;
    }

    memset(&ifr, 0, sizeof(ifr));
    strncpy(ifr.ifr_name, interface_name, IFNAMSIZ - 1);

    if (ioctl(socket_fd, SIOCGIFINDEX, &ifr) < 0) {
        perror("Erro ao obter o índice da interface\n");
        close(socket_fd);
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

    memset(&mr, 0, sizeof(mr));
    mr.mr_ifindex = ifr.ifr_ifindex;
    mr.mr_type = PACKET_MR_PROMISC;
    if (setsockopt(socket_fd, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr)) < 0) {
        perror("Erro ao setar socket\n");
        return -1;
    }

    return socket_fd;
}