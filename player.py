import socket
import json
import threading
import time
from the_ai import move_extractor

class Player:
    """
    The Player class is used to subscribe to the game server as well
    as responding to pings and applying the AI's algorithm moves
    """
    def __init__(self, sub_address, game_address, name, matricules):
        self.sub_address = sub_address #input an adress tuple(host, port) for subscribtion processes and Player info passing to game server
        self.game_address = game_address #input an adress tuple(host, port) for ping and game comunnication
        self.name = name #name of the Player
        self.matricules = matricules #List of the two student matricules in str type

    def server_response(self, s):
        """
        This function is used to decode a message (bits ==> json ==> str) from the server.
        Returns the message in str type.
        """
        server_resp = s.recv(2048).decode()
        msg = json.loads(server_resp)
        return(msg)

    def player_response(self, client, response):
        """
        This function is used to encode and send a message (str ==> json ==> str) to the server.
        """
        
        resp = json.dumps(response).encode('utf8')
        total = 0
        while total < len(resp):
            sent = client.send(resp[total:])
            total += sent

    def sub(self):
        """
        This function passes the subscription request to the game server.
        """
        data = {"request": "subscribe", "port": self.game_address[1],"name": self.name, "matricules": self.matricules}
        print("INFO:inscription:sent player creds: ")
        print(data)
        port = self.sub_address[1]
        with socket.socket() as sub_sock: #open subscription socket and closes when exits
            sub_sock.connect(self.sub_address)
            self.player_response(sub_sock, data)
            print("INFO:inscription:player " + self.name + ':' + self.server_response(sub_sock)["response"])

    def begin(self):
        """
        This function initializes a server socket to communicate with the game server.
        """
        self.player_sock = socket.socket()
        self.player_sock.bind(self.game_address)
        self.player_sock.listen()
    
    def comm(self):
        """
        This function handles communication requests from the game server
        """
        while True:
            (client, address) = self.player_sock.accept()
            with client:
                msg = self.server_response(client)
                if msg['request'] == 'ping':
                    self.player_response(client, {'response': 'pong'})
                    print("INFO:player and server are playing at ping pong")
                elif msg['request'] == 'play':
                    print("GAME:\nLives left: " + str(msg['lives']) + "\nErrors: " + str(msg['errors']) + "\nGame state: " + str(msg['state']))
                    the_move_played = move_extractor(msg['state'])
                    self.player_response(client, {"response": "move","move": the_move_played, "message": "L'important c'est de participer ;p"})
    
    def thread(self):
        """
        This function creates a thread using the comm() fuction.
        """
        threading.Thread(target = self.comm).start()



if __name__ == "__main__":

    player1 = Player(("127.0.0.1", 3000), ("127.0.0.1", 8080), "TheBest", ["20269", "20269"])

    player1.sub()
    player1.begin()
    player1.thread()

    time.sleep(3)

    player2 = Player(("127.0.0.1", 3000), ("127.0.0.1", 5050), "TheBetter", ["18021", "23012"])

    player2.sub()
    player2.begin()
    player2.thread()