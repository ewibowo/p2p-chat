import clientlib
from clientlib import Peer
import threading
import socklib
import rsalib
import sys

HOST = socklib.HOST
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else socklib.PORT

peers = []

### Server Functions ###

def handle_client(sock, addr):
    """ Receive data from the clientlib via sock and echo it back """
    try:
        command = socklib.recv_msg(sock)  # Blocks until received complete message
        
        if command.lower() == "identify":
            response = identify()
        else:
            command_str = decrypt_command_peer(command).decode('utf-8')
            command_arr = command_str.split()
            
            action = command_arr[0].lower()
         
            if action == "register":
                ip_addr = command_arr[0].lower()
                port = command_arr[1].lower()
                
                peer = Peer(ip_addr, port)
                add_peer(peer)
                
                response = peer.ip_addr + " " + peer.port + " has been registered." 
            elif action == "deliver":
                
                response = ' '.join(command_arr[1:]) + " received OK"
                print(response)
             
        
        socklib.send_msg(sock, str(response))  # Blocks until sent
    except (ConnectionError, BrokenPipeError):
        print('Socket error')
    finally:
        sock.close()
        
def decrypt_command_peer(cipher_command):
    private_key = rsalib.get_private_key(HOST, PORT)
    plain_command = private_key.decrypt(eval(cipher_command))
    return plain_command
        
def identify():
    public_key_str = rsalib.get_public_key_str(HOST, PORT)
    return public_key_str

def start_server():
    listen_sock = socklib.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('\nThe server on this node listening on {}'.format(addr))
    rsalib.create_private_key_file(HOST, PORT)
    
    while True:
        client_sock, addr = listen_sock.accept()
        #print('Connection from {}'.format(addr))
        handle_client(client_sock, addr)

### Node functions ###

def menu():
    print(""" --- MENU ---
    1. Register a peer
    2. Send a message
    3. Exit
    """)
    choice = input("Please choose: ")
    return choice

def register():
    ip_addr = input("IP address? ")
    port = input ("Port no? ")
    new_peer = Peer(ip_addr, port)
    
    add_peer(new_peer)
    
    this_node = HOST + " " + str(PORT)
    
    # If the current peer does not have a public key, identify first to obtain the public key
    if new_peer.public_key_filename == "":
        clientlib.client_connect(new_peer, "identify")
    
    clientlib.client_connect(new_peer, "register " + this_node)

def add_peer(new_peer):
    global peers
    
    # Check whether this current_peer was already registered before
    found = False
    current_peer = None
    for current_peer in peers:
        if current_peer.ip_addr == new_peer.ip_addr and current_peer.port == new_peer.port:
            found = True
            break
                
    if not found:        
        peers += [new_peer]
        print(new_peer.ip_addr + " " + new_peer.port + " has been added OK.")
        current_peer = new_peer
    
    
        
def send_msg():
    peer = list_peers()
    print("Type message, enter to send: ")
    msg = input()
    clientlib.client_connect(peer, "deliver " + msg)

def list_peers():
    counter = 1
    print("--- PEER LIST ---")
    for peer in peers:
        print(str(counter) + ". IP address: " + peer.ip_addr + " Port:" + peer.port + " Public key: " + peer.public_key_filename)
        counter += 1
    choice = int(input("Please choose a destination peer: "))
    return peers[choice-1]

if __name__ == '__main__':
  
    
    server_thread = threading.Thread(target=start_server,
                                       args=[],
                                       daemon=True)
    server_thread.start()
    while True:
        choice = str(menu())
        if choice == "1":
            register()
        elif choice == "2":
            send_msg()
        else:
            print("Done.")
            break
            