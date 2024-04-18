#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/ethernet.h>
#include <linux/if_packet.h>
#include <linux/if.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <dirent.h>

#include "socket.h"

int main() {
    int client_socket = create_socket("enp1s0");
    char buffer[1024] = {0};
    int status;

    status = connect(client_socket, NULL, 0);
    if (status < 0) {
        perror("Erro ao conectar\n");
        return -1;
    }

    recv(client_socket, buffer, 1024, 0);
    printf("%s\n", buffer);

    close(client_socket);

    return 0;
}
