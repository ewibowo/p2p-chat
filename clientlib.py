import sys, socket
import socklib
import rsalib
import pickle

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = socklib.PORT

class Peer:
    def __init__(self, ip_addr, port, public_key_filename=""):
        self.ip_addr = ip_addr
        self.port = port
        self.public_key_filename = public_key_filename

def client_connect(peer, command):
    command = command.lower()
    if command == "identify":
        identify_peer(peer, command)
    else: 
        encrypt_command_peer(peer, command)
        
def encrypt_command_peer(peer, command):
    try:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
        sock.connect((peer.ip_addr, int(peer.port)))
        print('\nConnected to {}:{}'.format(HOST, PORT))
        
        peer_public_key = rsalib.get_peer_public_key(peer.public_key_filename)
        
        cipher_command = peer_public_key.encrypt(command.encode('utf-8'), 32)
        
        socklib.send_msg(sock, str(cipher_command))  # Blocks until sent
        response = socklib.recv_msg(sock)  # Block until received complete message
        print('Received from server: \n' + response)
        
    except ConnectionError:
        print('Socket error')
    finally:
        sock.close()
        #print('Closed connection to server\n')
    
def identify_peer(peer, msg):
    try:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
        sock.connect((peer.ip_addr, int(peer.port)))
        print('\nConnected to {}:{}'.format(HOST, PORT))
        
        socklib.send_msg(sock, msg)  # Blocks until sent
        print('Sent message to server: {}'.format(msg))
        response = socklib.recv_msg(sock)  # Block until
                                         # received complete
                                         # message
                                         
        peer.public_key_filename = rsalib.save_public_key(peer.ip_addr, peer.port, response)
        print('Received from server: \n' + response)
    except ConnectionError:
        print('Socket error')
    finally:
        sock.close()
        #print('Closed connection to server\n')
