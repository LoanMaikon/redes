CC = gcc
CFLAGS = -Wall -g

COMMON_OBJS = obj/socket_handler.o obj/common_packets.o obj/basic_for_packets.o

all: server client

server: obj/server.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) -o server obj/server.o $(COMMON_OBJS)

client: obj/client.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) -o client obj/client.o $(COMMON_OBJS)

obj/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@ $(LFLAGS)

clean:
	rm -f server client obj/*.o
