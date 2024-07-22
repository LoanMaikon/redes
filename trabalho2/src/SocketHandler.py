import socket

class SocketHandler:
    def __init__(self, addr):
        self.sock = self.create_socket()
        self.sock.bind(addr)
    
    '''
    Create a DGRAM socket
    '''
    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    '''
    Send a packet to an address
    '''
    def send_packet(self, packet, addr):
        self.sock.sendto(packet, addr)
    
    '''
    Receive packet from the socket and return
    '''
    def receive_packet(self, socket_buffer_size):
        try:
            data, addr = self.sock.recvfrom(socket_buffer_size)
            return data, addr
        except:
            return None, None
        
    '''
    Wait until receive packet
    '''
    def wait_receive_packet(self, socket_buffer_size):
        while True:
            data, addr = self.receive_packet(socket_buffer_size)
            if data:
                return data, addr
    
    '''
    Set the socket timeout
    '''
    def setTimeOut(self, timeout):
        self.sock.settimeout(timeout)
