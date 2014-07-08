import sys
import random
import math

w, h = map(int, input().split())
jumps = int(input())
x, y = map(int, input().split())
px, py = x, y
search_zone = [(x, y) for x in range(w) for y in range(h)]

def distance(ax, ay, bx, by):
    return math.sqrt((bx - ax)**2 + (by - ay)**2)

def around(zone, x, y):
    return [(x, y) for  (x, y) in (
        (x, y - 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
        (x, y + 1),
        (x - 1, y + 1),
        (x - 1, y),
        (x - 1, y - 1)) if (x, y) in zone]

def centroid(zone):
    sumx, sumy = (0, 0)
    for x, y in zone:
        sumx += x
        sumy += y
    print(sumx / len(zone), sumy / len(zone), file=sys.stderr)
    result = round(sumx / len(zone)), round(sumy / len(zone))
    if result not in zone: result = random.choice(around(zone, *result))
    return result

while True:
    temperature = input()
    if temperature == "UNKNOWN": pass
    elif temperature == "WARMER":
        search_zone = [(szx, szy) for (szx, szy) in search_zone if distance(szx, szy, x, y) < distance(szx, szy, px, py)]
    elif temperature == "COLDER":
        search_zone = [(szx, szy) for (szx, szy) in search_zone if distance(szx, szy, x, y) > distance(szx, szy, px, py)]
    elif temperature == "SAME":
        search_zone = [(szx, szy) for (szx, szy) in search_zone if distance(szx, szy, x, y) == distance(szx, szy, px, py)]
    px, py = x, y
    x, y = centroid(search_zone)
    search_zone = [(szx, szy) for (szx, szy) in search_zone if (szx, szy) != (x, y)]
    print(w, h, jumps, x, y, temperature, len(search_zone), file=sys.stderr)
    print(x, y)
