# p2p-chat

The chat server listens until a client connects and sends a bytes string. Each node has both a server process and a client process. 

Implementation:

1.	Communication takes place over TCP.

2.	The server listens for the connection.

3.	The client initiates a chat session by creating a socket connection to the server.

4. The server accepts the connection request.

5.	The client sends a bytes string to the server. Then, it will listen for a reply from the server.

6.	When the server receives the bytes string from the client, it reply a bytes string back to the client.

7.	When the client has received the reply bytes string from the server, it will close its socket to end the session.

The nodes (sender and recipient) use the public key infrastructure for encrypting messages.
![](https://github.com/ewibowo/p2p-chat/raw/master/PKI.png)

```
For example, to run two nodes and register a peer.

On Node 1 (192.168.0.1):
python3 node.py 1111
 --- MENU ---
    1. Register a peer
    2. Send a message
    3. Exit
    
On Node 2 (192.168.0.2):
python3 node.py 2222
--- MENU ---
    1. Register a peer
    2. Send a message
    3. Exit
Please choose: 1
Peer IP address? 192.168.0.1
Peer Port no? 1111
Send message to peer: identify
Received from server: 
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDAB7NUoP8KT/XpyBF2qJIF+QXA
Nce0iJMPa26KBGXVSrxEyyGYOsaDg98DXZ8ru62dLVhBs9AHpp1NJg5O8sSyeSzJ
CO6rYkBAZxX22DCosQYkc71NEud+M5fRrjcwYjcBIzuv+0DnVoImMdh3jF5mz3Zu
FFfWPQVNUlFSLy2WSwIDAQAB
-----END PUBLIC KEY-----
192.168.0.1 has been successfully registered.
```
