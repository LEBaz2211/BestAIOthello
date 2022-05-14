import socket
import threading
import json

def server_response(sock):
    """
    This function is used to decode a message (bits ==> json ==> str) from the server.
    Returns the message in str type.
    """
    server_resp = sock.recv(2048).decode()
    msg = json.loads(server_resp)
    return(msg)

def player_response(client, response):
    """
    This function is used to encode and send a message (str ==> json ==> str) to the server.
    """
    
    resp = json.dumps(response).encode('utf8')
    total = 0
    while total < len(resp):
        sent = client.send(resp[total:])
        total += sent

def begin_server( game_address):
    """
    This function initializes a server socket to communicate with the game server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(game_address)
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = server_response(conn)
                if not data:
                    break
    return data, conn