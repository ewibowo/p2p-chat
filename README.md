# p2p-chat

The chat server should listen until a client connects and sends a bytes string, waiting to reply back to the chat client. These rules are as follows:

1.	Communication will take place over TCP.

2.	The client will initiate a chat session by creating a socket connection to the server.

3.	The server will accept the connection and listen for the client to send a bytes string.

4.	The client will send a bytes string to the server.

5.	Once it sends the bytes string, the client will listen for a reply from the server

6.	When it receives the bytes string from the client, the server can send a reply bytes string back to the client.

7.	When the client has received the reply bytes string from the server, it will close its socket to end the session.

The challenge here is how the server and the client will know when a complete message has been sent. Remember that an application sees a TCP connection as an endless stream of bytes, so we need to decide what in that byte stream will signal the end of a message. This problem is called framing. For  this chat applications, we'll be using the UTF-8 character set to send messages. The null byte isn't used in any character in UTF-8 except for the null byte itself, so it makes a good delimiter.

Each node has both a chat server and a chat client. The server will listen to a specific TCP port; whereas the client can initiate the socket connection.
```
For example, to run two nodes:

On Node 1 (192.168.0.1):
python3 node.py 1111
 --- MENU ---
    1. Register a peer
    2. Send a message
    3. Exit
    
On Node 2 (192.168.0.2):
Node 2: python3 node.py 2222
--- MENU ---
    1. Register a peer
    2. Send a message
    3. Exit
    
Please choose: 1
IP address? 192.168.0.1
Port no? 1111
192.168.0.1 1111 has been added OK.
Sent message to server: identify
Received from server: 
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDAB7NUoP8KT/XpyBF2qJIF+QXA
Nce0iJMPa26KBGXVSrxEyyGYOsaDg98DXZ8ru62dLVhBs9AHpp1NJg5O8sSyeSzJ
CO6rYkBAZxX22DCosQYkc71NEud+M5fRrjcwYjcBIzuv+0DnVoImMdh3jF5mz3Zu
FFfWPQVNUlFSLy2WSwIDAQAB
-----END PUBLIC KEY-----
Received from server: 
192.168.0.1 has been successfully registered.
```
