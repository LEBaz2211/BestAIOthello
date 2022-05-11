from player import Player

ready_player_one = Player(("127.0.0.1", 3000), ("127.0.0.1", 8080), "LEBaz", ["20269", "18402"])

ready_player_one.sub()
ready_player_one.begin()
ready_player_one.thread()