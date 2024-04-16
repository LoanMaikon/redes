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
    int server_socket = create_socket("eth0");
    int new_socket;
    char *message = "hello";

    listen(server_socket, 5);

    new_socket = accept(server_socket, NULL, NULL);

    send(new_socket, message, strlen(message), 0);

    close(server_socket);

    return 0;
}