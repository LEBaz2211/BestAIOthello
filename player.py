import socket
import json
import threading



class Player:
    """
    The Player class is used to subscribe to the game server as well
    as responding to pings and applying the AI's algorithm moves
    """
    def __init__(self, sub_adress, game_adress, name, matricules):
        self.sub_adress = sub_adress #input an adress tuple(host, port) for subscribtion processes and Player info passing to game server
        self.game_adress = game_adress #input an adress tuple(host, port) for ping and game comunnication
        self.name = name #name of the Player
        self.matricules = matricules #List of the two student matricules

    def server_response(self, s):
        server_resp = s.recv(2048).decode()
        msg = json.loads(server_resp)
        return(msg)

    def player_response(self, client, response):
        resp = json.dumps(response).encode('utf8')
        total = 0
        while total < len(resp):
            sent = client.send(resp[total:])
            total += sent
    