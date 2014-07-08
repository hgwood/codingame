import sys

w, h = map(int, input().split())
jumps = int(input())
x, y = map(int, input().split())
search_zone = [[0, 0], [w - 1, h - 1]]

while True:
    bomb_direction = input()
    print(w, h, jumps, x, y, bomb_direction, search_zone, file=sys.stderr)
    if "U" in bomb_direction: search_zone[1][1] = y - 1
    if "D" in bomb_direction: search_zone[0][1] = y + 1
    if "L" in bomb_direction: search_zone[1][0] = x - 1
    if "R" in bomb_direction: search_zone[0][0] = x + 1
    x = search_zone[0][0] + (search_zone[1][0] - search_zone[0][0]) / 2
    y = search_zone[0][1] + (search_zone[1][1] - search_zone[0][1]) / 2
    x, y = int(x), int(y)
    print(w, h, jumps, x, y, bomb_direction, search_zone, file=sys.stderr)
    print(x, y)
