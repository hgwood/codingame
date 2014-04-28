from itertools import *

# Debug helpers

import sys

def dump(*values, sep="\n"):
    print(*values, sep=sep, file=sys.stderr)

def fdump(func):
    def decorated(*args, **kwargs):
        dump(func.__name__, "called with", args, kwargs, sep=" ")
        result = func(*args, **kwargs)
        dump(func.__name__, "returned", result, sep=" ")
        return result
    return decorated


# Game

def merge(roads):
    return "".join(("0" if "0" in block else ".") for block in zip(*roads))

def detect_next_hole(road_ahead):
    position = road_ahead.find("0")
    distance = len(road_ahead.strip(".").split(".")[0])
    return position, distance

@fdump
def tree(speed, target_speed, distance):
    if speed < 1 or distance < 0: return None
    if distance == 0 and speed < target_speed: return None
    if distance == 0 and speed >= target_speed: return "JUMP"
    for speed_diff, action in reversed(((-1, "SLOW"), (0, "WAIT"), (+1, "SPEED"))):
        new_speed = speed + speed_diff
        if tree(new_speed, target_speed, distance - new_speed): 
            return action
    return None

def play(nbikes, mbikes, roads, speed, bikes):
    x = bikes[0][0]
    ys = tuple(y for _, y, active in bikes if active)
    roads = tuple(roads[y] for y in ys)  
    road = merge(roads)
    road_ahead = road[x + 1:]
    hole_distance, hole_length = detect_next_hole(road_ahead)
    dump(nbikes, mbikes, roads, speed, bikes, road, road_ahead, hole_distance, hole_length)
    
    # Cas limites
    if hole_distance == -1:
        return "WAIT"
    if speed == 0:
        return "SPEED"
    
    return tree(speed, hole_length + 1, hole_distance) or "JUMP"


if __name__ == "__main__":

    def init_input():
        nbikes = int(input())
        mbikes = int(input())
        roads = tuple(input() for _ in range(4))
        return nbikes, mbikes, roads
    
    def turn_input(nbikes):
        speed = int(input())
        bikes = tuple(tuple(map(int, input().split())) for _ in range(nbikes))
        return speed, bikes
    
    nbikes, mbikes, roads = init_input()
    while True:
        speed, bikes = turn_input(nbikes)
        print(play(nbikes, mbikes, roads, speed, bikes))
