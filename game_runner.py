from player import Player
import threading
import atexit
#              subscription address      game address
#                       |                     |
#                       v                     v
player1 = Player(("127.0.0.1", 3000), ("127.0.0.1", 8080), "TheBest, maybe?", ["20269", "18402"])

player1.sub()
t = threading.Thread(target = player1.run)
t.start()
atexit.register(player1.terminate, )