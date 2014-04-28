from itertools import *

# Debug helpers

import sys

def dump(*values, sep="\n"):
    print(*values, sep=sep, file=sys.stderr)

def fdump(func):
    def decorated(*args, **kwargs):
        dump(func.__name__, "called with", args, kwargs)
        result = func(*args, **kwargs)
        dump(func.__name__, "returned", result)
        return result
    return decorated


# I/O helpers

def read(input, count):
    yield from map(int, islice(input, count))

def init_input(input):
    yield from read(input, 3)

def turn_input(input):
    yield from read(input, 2)


# Game

def play(road, gap, platform, speed, position):
    dump(road, gap, platform, speed, position)
    if position < road - 1 and speed < gap + 1:
        return "SPEED"
    elif position == road - 1:
        return "JUMP"
    elif position >= road or speed > gap + 1:
        return "SLOW"
    else:
        return "WAIT"


if __name__ == "__main__":
    def stdin():
        while True: yield input()
    road, gap, platform = init_input(stdin())
    while True:
        speed, position = turn_input(stdin())
        print(play(road, gap, platform, speed, position))
