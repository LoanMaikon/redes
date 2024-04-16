CFLAGS = -Wall
LDFLAGS = -lm
CC = gcc
objects = client server *.o
all: client server
    

client: client.o socket.o
	$(CC) -o client client.o socket.o $(LDFLAGS)

server: server.o socket.o
	$(CC) -o server server.o socket.o $(LDFLAGS)


socket.o: socket.c
	$(CC) -c $(CFLAGS) socket.c

client.o: client.c
	$(CC) -c $(CFLAGS) client.c

server.o: server.c
	$(CC) -c $(CFLAGS) server.c

clean:
	rm -f $(objects)
