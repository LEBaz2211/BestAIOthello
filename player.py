import socket
import json
import threading
import time
from the_ai import move_extractor
from socket_handling import server_response, player_response
import time
import atexit

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
        self._running = True


    def sub(self):
        """
        This function passes the subscription request to the game server.
        """
        data = {"request": "subscribe", "port": self.game_address[1],"name": self.name, "matricules": self.matricules}
        print("INFO:inscription:sent player creds: ")
        print(data)
        with socket.socket() as sub_sock: #open subscription socket and closes when exits
            try:
                sub_sock.connect(self.sub_address)
                player_response(sub_sock, data)
                print("INFO:inscription:player " + self.name + ':' + server_response(sub_sock)["response"])
            except ConnectionRefusedError:
                print("The game server isn't open yet")
    
    def terminate(self):
        self._running = False

    def run(self):
        with socket.socket() as player_sock:
            player_sock.bind(self.game_address)
            state0 = None
            state1 = None
            while True:
                if state1 is not None:
                    state0 = state1
            # Set timeout period
                player_sock.settimeout(5) 
                while self._running:
                    player_sock.listen()
                    try:
                        (conn, address) = player_sock.accept()
                    except TimeoutError:
                        print("Waiting for game server to send a request")
                        self.test_for_ping(player_sock)
                    try:
                        msg = server_response(conn)
                        if msg['request'] == 'ping':
                            self.pong(conn)
                        elif msg['request'] == 'play':
                            self.move(conn, msg)
                        break
                    except socket.timeout and json.decoder.JSONDecodeError:
                        continue
        return
    
    def test_for_ping(self, player_sock):
        while True:
            player_sock.settimeout(5)
            while self._running:
                player_sock.listen()
                try:
                    (conn, address) = player_sock.accept()
                    msg = server_response(conn)
                    if msg['request'] == 'ping':
                        self.pong(conn)
                        return
                    break
                except socket.timeout or TimeoutError:
                    continue


    # def comm(self):
    #     """
    #     This function handles communication requests from the game server
    #     """
    #     while True:
    #         msg, conn = begin_server(self.game_address)
    #         if not msg:
    #             self.comm()
    #             print('yes')
    #             break
    #         start = time.time()
    #         print(msg)
    #         if msg['request'] == 'ping':
    #             self.pong(conn)
    #             end = time.time()
    #         elif msg['request'] == 'play':
    #             self.move(conn, msg)
    #             end = time.time()
    #     if end is not None: print("Time of execution:", end-start)

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
    t = threading.Thread(target = player1.run)
    t.start()
    atexit.register(player1.terminate, )

    player2 = Player(("127.0.0.1", 3000), ("127.0.0.1", 5000), "TheBetter", ["15254"])

    player2.sub()
    t = threading.Thread(target = player2.run)
    t.start()
    atexit.register(player2.terminate, )