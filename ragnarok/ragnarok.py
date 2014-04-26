# Algorithm
#
# if next to giant and enough giants in range
#   strike
# if is on centroid or next position towards centroid is dangerous
#   if current position is dangerous
#     move to a random safe neighboring position
#   else
#     wait
# else
#   move toward centroid

import random
import sys


def parse(line):
    return map(int, line.split())

def is_in_zone(x, y, gx, gy, radius):
    return y - radius <= gy <= y + radius and x - radius <= gx <= x + radius
    
def is_next_to(x, y, gx, gy):
    return is_in_zone(x, y, gx, gy, 1)

def is_in_strike_zone(x, y, gx, gy):
    return is_in_zone(x, y, gx, gy, 4)

def centroid(positions): # centroid == barycentre
    sumx, sumy = (0, 0)
    for x, y in positions:
        sumx += x
        sumy += y
    return round(sumx / len(positions)), round(sumy / len(positions))

def direction_to(fromx, fromy, tox, toy):
    if fromx == tox and fromy == toy:
        return "WAIT", fromx, fromy
    newx, newy = fromx, fromy
    result = ""
    if fromy < toy:
        newy += 1
        result = "S"
    elif fromy > toy:
        newy -= 1
        result = "N"
    if fromx < tox:
        newx += 1
        result += "E"
    elif fromx > tox:
        newx -= 1
        result += "W"
    return result, newx, newy

def is_safe(x, y, giant_positions):
    if (x, y) in giant_positions: return False
    neighbors = (
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1))
    return not any((nx,ny) in giant_positions for nx,ny in neighbors)

def is_in_map(x, y):
    return 0 <= x < 40 and 0 <= y < 18

def free_neighboring_positions(x, y, giant_positions):
    neighbors = (
        ("NW", x - 1, y - 1),
        ("W", x - 1, y),
        ("SW", x - 1, y + 1),
        ("N", x, y - 1),
        ("S", x, y + 1),
        ("NE", x + 1, y - 1),
        ("E", x + 1, y),
        ("SE", x + 1, y + 1))
    return [(dir,nx,ny) for dir,nx,ny in neighbors if is_safe(nx,ny,giant_positions)]

x, y = parse(input())

while True:
    hammer_power, number_of_giants = parse(input())
    kills_by_strike = min(number_of_giants, number_of_giants // hammer_power + 1)
    giant_positions = [tuple(parse(input())) for _ in range(number_of_giants)]
    number_of_giants_inside_strike_zone = sum(1 for gx, gy in giant_positions if is_in_strike_zone(x, y, gx, gy))
    print("hammer power", hammer_power, file=sys.stderr)
    print("number_of_giants", number_of_giants, file=sys.stderr)
    print("kills_by_strike", kills_by_strike, file=sys.stderr)
    print("number_of_giants_inside_strike_zone", number_of_giants_inside_strike_zone, file=sys.stderr)
    have_to_move = False
    if any(is_next_to(x, y, gx, gy) for gx, gy in giant_positions):
        if number_of_giants_inside_strike_zone >= kills_by_strike:
            print("STRIKE")
            continue
        else:
            have_to_move = True
    cx, cy = centroid(giant_positions)
    direction, newx, newy = direction_to(x, y, cx, cy)
    if any(is_next_to(newx, newy, gx, gy) for gx, gy in giant_positions):
        direction = "WAIT"
    if direction == "WAIT" and have_to_move:
        print(x, y, giant_positions, file=sys.stderr)
        fn = free_neighboring_positions(x, y, giant_positions)
        if len(fn) == 0:
            print(x, y, newx, newy, fn, file=sys.stderr)
            print("STRIKE")
            continue
        direction, newx, newy = random.choice(fn)
    x, y = newx, newy
    print(direction)