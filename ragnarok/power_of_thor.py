import sys

def parse(line):
    return map(int, line.split())

lx, ly, tx, ty = parse(input())
x, y = tx, ty

while True:
    e, = parse(input())
    result = ""
    if y < ly:
        y += 1
        result = "S"
    elif y > ly:
        y -= 1
        result = "N"
    if x < lx: 
        x += 1
        result += "E"
    elif x > lx: 
        x -= 1
        result += "W"
    print(result)
