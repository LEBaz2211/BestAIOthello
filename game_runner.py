from player import Player

ready_player_one = Player(("172.17.10.40", 3000), ("172.17.10.40", 8001), "The Best, maybe?", ["20269", "18402"])

ready_player_one.sub()
ready_player_one.begin()
ready_player_one.thread()