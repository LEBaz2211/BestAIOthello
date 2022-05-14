import socket
import json
import threading
import time
from the_ai import move_extractor
from socket_handling import server_response, begin_server, player_response
import time

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
            player_response(sub_sock, data)
            print("INFO:inscription:player " + self.name + ':' + server_response(sub_sock)["response"])
    
    def comm(self):
        """
        This function handles communication requests from the game server
        """
        while True:
            msg, conn = begin_server(self.game_address)
            if not msg:
                self.comm()
                print('yes')
                break
            start = time.time()
            print(msg)
            if msg['request'] == 'ping':
                self.pong(conn)
                end = time.time()
            elif msg['request'] == 'play':
                self.move(conn, msg)
                end = time.time()
        if end is not None: print("Time of execution:", end-start)

    def pong(self, conn):
        player_response(conn, {'response': 'pong'})
        print("INFO:player and server are playing at ping pong")

    def move(self, conn, msg):
        print("GAME:\nLives left: " + str(msg['lives']) + "\nErrors: " + str(msg['errors']) + "\nGame state: " + str(msg['state']))
        the_move_played = move_extractor(msg['state'])
        player_response(conn, {"response": "move","move": the_move_played, "message": "L'important c'est de participer ;p"})

    # def comm(self):
    #     """
    #     This function handles communication requests from the game server
    #     """
    #     while True:
    #         (client, address) = self.player_sock.accept()
    #         with client:
    #             msg = server_response(client)
    #             if msg['request'] == 'ping':
    #                 player_response(client, {'response': 'pong'})
    #                 print("INFO:player and server are playing at ping pong")
    #             elif msg['request'] == 'play':
    #                 print("GAME:\nLives left: " + str(msg['lives']) + "\nErrors: " + str(msg['errors']) + "\nGame state: " + str(msg['state']))
    #                 the_move_played = move_extractor(msg['state'])
    #                 player_response(client, {"response": "move","move": the_move_played, "message": "L'important c'est de participer ;p"})
    
    def thread(self):
        """
        This function creates a thread using the comm() fuction.
        """
        threading.Thread(target = self.comm).start()



if __name__ == "__main__":

    player1 = Player(("127.0.0.1", 3000), ("127.0.0.1", 8080), "TheBest", ["20269", "20269"])

    player1.sub()
    player1.thread()

    time.sleep(2)

    player2 = Player(("127.0.0.1", 3000), ("127.0.0.1", 5000), "TheBetter", ["15354", "18335"])

    player2.sub()
    player2.thread()