# Algorithm
#
# if enough giants in range or no safe positions to go to (including current)
#   strike
# else
#   move to the safe position that's closest to the centroid of the giants

from itertools import product
import math


def collect(decorated):
    return lambda *args, **kwargs: tuple(decorated(*args, **kwargs))

def offset(numbers, by):
    return (i + by for i in numbers)

def centered_range(center, radius):
    return offset(range(radius * 2 + 1), by=center-radius)

@collect
def area_around(center, radius=1):
    return product(*(centered_range(coord, radius) for coord in center))

@collect
def areas_around(centers, radius=1):
    for center in centers: yield from area_around(center, radius)

def rounded_average(numbers):
    return round(sum(numbers) / len(numbers))

def transposed(points):
    return zip(*points)

@collect
def centroid(points):
    return (rounded_average(dimension) for dimension in transposed(points))

@collect
def vector(here, there):
    points = here, there
    return (abs(a - b) for a, b in transposed(points))

def distance(here, there):
    return max(vector(here, there))

def geographic_distance(here, there):
    return sum(vector(here, there))

def closest_to(reference, among):
    return min(among, key=lambda point: geographic_distance(reference, point))

def legal(position):
    x, y = position
    return 0 <= x < 40 and 0 <= y < 18

def play(thor, hammer, giants):

    def optimal_direction():
        def reasonable(position):
            return legal(position) and position not in areas_around(giants)
        def direction_to(position):
            if position == thor: return "WAIT"
            (tx, ty), (px, py) = thor, position
            return {py < ty: "N", ty == py: "", py > ty: "S"}[True] \
                 + {px < tx: "W", tx == px: "", px > tx: "E"}[True]
        potentials = tuple(filter(reasonable, area_around(thor)))
        if not potentials: return None
        return direction_to(closest_to(centroid(giants), among=potentials))

    def enough_giants_in_range():
        minimum_kills_required_on_next_strike = math.ceil(len(giants) / hammer)
        strike_zone = area_around(thor, radius=4)
        giants_in_range = sum(1 for giant in giants if giant in strike_zone)
        return giants_in_range >= minimum_kills_required_on_next_strike
    if enough_giants_in_range(): return "STRIKE"
    return optimal_direction() or "STRIKE"

def spawn_thor(position):
    x, y = position
    def move(direction=""):
        nonlocal x, y
        if direction in ("WAIT", "STRIKE"): direction = ""
        if "N" in direction: y -= 1
        elif "S" in direction: y += 1
        if "W" in direction: x -= 1
        elif "E" in direction: x += 1
        return x, y
    return move

if __name__ == "__main__":
    def parse(line):
        return tuple(map(int, line.split()))
    thor = spawn_thor(parse(input()))
    while True:
        hammer, ngiants = parse(input())
        giants = tuple(parse(input()) for _ in range(ngiants))
        move = play(thor(), hammer, giants)
        print(move)
        thor(move)
