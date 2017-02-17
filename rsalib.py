from Crypto.PublicKey import RSA
from Crypto import Random
import os

### PRIVATE KEY ###

def get_private_key_filename(HOST, PORT):
    private_key_filename = 'server-' + HOST +'-' + str(PORT) + '-private_key.pem'
    return private_key_filename

def create_private_key_file(HOST, PORT):
    private_key_filename = get_private_key_filename(HOST, PORT)
    # If the private key file does not exist, create it 
    if not os.path.exists(private_key_filename):
        random_generator = Random.new().read
        private_key = RSA.generate(1024, random_generator)
        f = open(private_key_filename,'wb')
        f.write(private_key.exportKey('PEM'))
        f.close()

def get_private_key_str(HOST, PORT):
    private_key_filename = get_private_key_filename(HOST, PORT)
    
    if not os.path.exists(private_key_filename):
        create_private_key_file(HOST, PORT)
    
    f = open(private_key_filename,'rb')
    private_key_str = f.read().decode()
    f.close()
    return private_key_str

def get_private_key(HOST, PORT):
    private_key_str = get_private_key_str(HOST, PORT)
    private_key = RSA.importKey(private_key_str)
    return private_key

### PUBLIC KEY ###

def get_public_key_filename(HOST, PORT):
    public_key_filename = 'server-' + HOST +'-' + str(PORT) + '-public_key.pem'
    return public_key_filename

def create_public_key_file(HOST, PORT):
    public_key_filename = get_public_key_filename(HOST, PORT)
    # If the private key file does not exist, create it 
    if not os.path.exists(public_key_filename):
        public_key = get_private_key(HOST, PORT).publickey()
        f = open(public_key_filename,'wb')
        f.write(public_key.exportKey('PEM'))
        f.close()

def get_public_key_str(HOST, PORT):
    public_key_filename = get_public_key_filename(HOST, PORT)
    
    # If the public key file does not exist, create it 
    if not os.path.exists(public_key_filename):
        create_public_key_file(HOST, PORT)
    
    
    f = open(public_key_filename,'rb')
    public_key_str = f.read().decode()
    f.close()
    return public_key_str

def get_public_key(HOST, PORT):
    public_key = RSA.importKey(get_public_key_str(HOST, PORT)) 
    return public_key

### PEER FUNCTIONS ###

def get_peer_public_key(public_key_filename):
    f = open(public_key_filename,'rb')
    public_key_str = f.read().decode()
    f.close()
    public_key = RSA.importKey(public_key_str) 
    return public_key

def save_public_key(ip_addr, port, public_key_str):
    public_key_filename = 'peer-' + ip_addr + '-' + str(port) + '-public_key.pem'
    if not os.path.exists(public_key_filename):
        f = open(public_key_filename,'wb')
        f.write(public_key_str.encode())
        f.close()
    
    return public_key_filename
