CFLAGS = -Wall
LDFLAGS = -lm
CC = gcc
objects = client server *.o
all: client server
     
client: client.o
	$(CC) -o client client.o $(LDFLAGS)

server: server.o
	$(CC) -o server server.o $(LDFLAGS)

client.o: client.c
	$(CC) -c $(CFLAGS) client.c

server.o: server.c
	$(CC) -c $(CFLAGS) server.c

clean:
	rm -f $(objects)
