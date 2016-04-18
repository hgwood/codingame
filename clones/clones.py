# pylint: disable=locally-disabled,missing-docstring,C0103,line-too-long

_, _, _, exit_floor, exit_pos, _, _, nb_elevators = [int(i) for i in input().split()]
elevators = dict(tuple(int(j) for j in input().split()) for _ in range(nb_elevators))
elevators[exit_floor] = exit_pos

while True:
    clone_floor, clone_pos, direction = input().split()
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)
    elevator_pos = elevators.get(clone_floor, clone_pos)
    if clone_pos < elevator_pos and direction == "LEFT" or clone_pos > elevator_pos and direction == "RIGHT":
        print("BLOCK")
    else:
        print("WAIT")
