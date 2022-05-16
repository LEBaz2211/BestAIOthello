from player import Player
import threading
import atexit
#              subscription address      game address
#                       |                     |
#                       v                     v
player1 = Player(("127.0.0.1", 3000), ("127.0.0.1", 8080), "The_potential_better", ["47369", "25314"])

player1.sub()
t = threading.Thread(target = player1.run)
t.start()
atexit.register(player1.terminate, )