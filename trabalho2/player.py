import socket
import time

def main():
    all_ports = [[i, i + 1] for i in range(1917, 1921)]
    all_ports[-1][1] = all_ports[0][0]  

    print("Digite o player que deseja ser: ")
    print("1 - Player 1")
    print("2 - Player 2")
    print("3 - Player 3")
    print("4 - Player 4")
    player = int(input())
    player_ports = all_ports[player - 1]

    addr1 = ("localhost", player_ports[0])
    addr2 = ("localhost", player_ports[1])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr1)
    sock.settimeout(0.1)

    if player == 1:
        msg = input("Digite a mensagem: ")

        recebeu = False
        while not recebeu:
            sock.sendto(msg.encode(), addr2)
            try:
                data, addr = sock.recvfrom(1024)
            except:
                continue
            
            if data:
                print("Mensagem recebida: ", data.decode())
                recebeu = True
        
    else:
        while True:
            data, addr = sock.recvfrom(1024)
            if data:
                print("Mensagem recebida: ", data.decode())
                break
        
        while True:
            sock.sendto(data, addr2)

if __name__ == "__main__":
    main()
