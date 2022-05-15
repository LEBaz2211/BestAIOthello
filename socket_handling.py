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