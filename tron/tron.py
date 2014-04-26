import collections
import operator
import sys
import uuid


# Optimization helpers.

def memoize(func):
    """Memoizing decorator for functions which take a grid as their first argument. Since a grid is 1) large and 
    2) made of lists and therefore not hashable, the id is used instead."""
    memo = {}
    def wrapper(grid, *args):
        key = (grid.id, args)
        if key not in memo:
            memo[key] = func(grid, *args)
        return memo[key]
    return wrapper


# Operations on grids.
#
# From the game's perspective, the grid is a 30 by 20 matrix in which player can move.
# From this program's perspective, a grid is a fully persistent* two-dimensional matrix of integers. Each positive 
# integer represents a different player, and -1 signifies the position is empty.
#
# In addition to the matrix itself, the grid data structure stores the width and height of the matrix as well as the
# empty value for fast and easy access.
#
# For optimization purposes, a grid instance is uniquely identified by a UUID, which is used as a key in the memoize
# decorator (see above).
#
# A persistent data structure was chosen because it provides both immutability, which is needed to simulate future
# moves without having to restore the grid after the simulation, and modification speed, since untouched parts of grids 
# are shared between instances (see the set_at function).
#
# * http://en.wikipedia.org/wiki/Persistent_data_structures 

Grid = collections.namedtuple("Grid", ("cells", "width", "height", "empty", "id"))

def make_grid(width, height, empty=-1):
    return Grid([[empty] * width for _ in range(height)], width, height, empty, uuid.uuid4())

def get_at(grid, x, y):
    return grid.cells[y][x]

def set_at(grid, value, x, y):
    """A new grid is returned but only the modified row is copied. Complexity is O(width + height)."""
    if get_at(grid, x, y) == value: return grid
    copy_of_grid = grid.cells[:] # shallow, rows are not copied, complexity O(height)
    copy_of_mutated_row = copy_of_grid[y][:] # shallow again, content of the row is not copied, complexity O(width)
    copy_of_mutated_row[x] = value
    copy_of_grid[y] = copy_of_mutated_row
    return Grid(copy_of_grid, grid.width, grid.height, grid.empty, uuid.uuid4())

def remove_all(grid, value):
    for position in all_positions_of(grid):
        if get_at(grid, *position) == value:
            set_at(grid, grid.empty, *position)

def contains(grid, x, y):
    return 0 <= x < grid.width and 0 <= y < grid.height

def max_distance_between_two_positions(grid):
    """This is the worst case scenario of pathfinding: reaching the destination requires to walk the entire grid!"""
    return grid.width * grid.height - 1

def is_empty(grid, position):
    return get_at(grid, *position) == grid.empty

def is_capturable(grid, position):
    return contains(grid, *position) and is_empty(grid, position)

@memoize # 50% speed boost ; number of calls decreased from 3587 to 600
def capturable_neighbors_of(grid, position):
    return tuple(neighbor for neighbor in neighbors_of(*position) if is_capturable(grid, neighbor))

def all_positions_of(grid):
    return ((x, y) for x in range(grid.width) for y in range(grid.height))

def all_capturable_positions_of(grid):
    return (position for position in all_positions_of(grid) if is_capturable(grid, position))


# Operation on positions.
#
# A position is a couple of XY coordinates on the grid, given the origin is the top left of the grid.

def neighbors_of(x, y):
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))

def relative_direction(reference, position):
    """Given two positions, return:
    - 0 if the second is directly on the left of the first
    - 1 if it's directly on the right
    - 2 if it's directly above
    - 3 if it's directly beneath
    - -1 if it's not adjacent"""
    return neighbors_of(*reference).index(position)


# Functions to evaluate how advantageous a position is.
#
# A position is better than another if it allows the player on it to reach more remote positions than its opponents. A 
# player that is closer to a given position is said to dominate that position.

def distances_from(grid, reference):
    """Compute the distance from a reference position to all other positions on the grid. Return a map from position
    to distance aka distance map or dmap for short."""
    distances = collections.defaultdict(lambda: max_distance_between_two_positions(grid), ((reference, 0),))
    unvisited = collections.deque((reference,))
    while unvisited:
        current = unvisited.popleft()
        for neighbor in capturable_neighbors_of(grid, current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                unvisited.append(neighbor)
    del distances[reference]
    return distances

def merge(condition, *dicts):
    """Merge several dicts into one. In case of conflict, condition is called with the key, the old value, and the new
    value as arguments: iff the result is truthy, the new value replaces the old one."""
    if len(dicts) == 1: return dicts[0]
    reference, *others = dicts
    for other in others:
        for key, value in other.items():
            if key not in reference or condition(key, reference[key], value):
                reference[key] = value
    return reference

def number_of_dominated_positions(grid, me, *opponents):
    dmaps_for_opponents = tuple(distances_from(grid, opponent) for opponent in opponents)
    merged_dmap = merge(lambda key, old, new: new < old, *dmaps_for_opponents)
    my_dmap = distances_from(grid, me)
    domination_map = {position: distance < merged_dmap[position] for position, distance in my_dmap.items()}
    return sum(1 for dominated in domination_map.values() if dominated)

def score_of(position, grid, *opponents):
    return number_of_dominated_positions(grid, position, *opponents)


# Game loop

def play(input_lines):
    moves = ("LEFT", "RIGHT", "UP", "DOWN")
    grid = make_grid(30, 20)
    eliminated_players = set()
    while True:
        number_of_players, my_id = parse(next(input_lines))
        player_positions = tuple(parse(next(input_lines))[2:] for _ in range(number_of_players))
        for index, position in enumerate(player_positions):
            if position == (-1, -1):
                if index not in eliminated_players:
                    eliminated_players.add(index)
                    remove_all(grid, index)
            else:
                grid = set_at(grid, index, *position)
        me = player_positions[my_id]
        opponents = player_positions[:my_id] + player_positions[my_id + 1:]
        scores = {score_of(position, grid, *opponents): position for position in capturable_neighbors_of(grid, me)}
        best_next_position = scores[max(scores)]
        best_move = moves[relative_direction(me, best_next_position)]
        yield best_move


# Input processing operations

def parse(line):
    return tuple(map(int, line.split()))


# Main

if __name__ == "__main__":
    def input_as_generator():
        while True: yield input()
    for move in play(input_as_generator()):
        print(move)