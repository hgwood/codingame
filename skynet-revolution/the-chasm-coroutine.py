def new_game(road_length, gap_length, platform_length):
    optimal_speed = gap_length + 1
    right_in_front_of_the_gap = road_length - 1
    def play(speed, bike):
        if bike is right_in_front_of_the_gap: return "JUMP"
        elif bike > road_length: return "SLOW"
        else: # bike on road
            if speed < optimal_speed: return "SPEED"
            elif speed > optimal_speed: return "SLOW"
            else: return "WAIT"
    speed, position = yield
    while True:
        speed, position = yield play(speed, position)

if __name__ == "__main__":
    read = lambda n: [int(input()) for _ in range(n)]
    game = new_game(*read(3))
    next(game)
    while True: print(game.send(read(2)))
