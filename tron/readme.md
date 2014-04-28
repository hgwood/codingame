# CodinGame - Tron Battle

Date: from 2014-10-01 to 2014-02-28
Ranking: #54

This piece of Python code is an AI for the Tron game. Given the number of players and their current positions on each
turn, it prints out the direction in which it thinks it's best to head to: either left, right, up or down. It considers
a position to be better than another if it allows the player on it to reach more remote positions than its opponents.
Performance was significant since the code had give an answer every 100ms at the least.

## Potential Improvements

- warrior: seek for occasions to corner and eliminate an opponent
- psychic: compute several moves in advance


## Interesting Bits

- Functional-style, even though it's in Python: no classes, one named tuple.
- The grid (the game board) is a fully persistent data structure:
    - Immutability makes it easy to simulate future moves (grid modifications) while ensuring the present grid remains
    in sync with the game.
    - Modification has a linear complexity of `O(width + height)` instead of the quadratic `O(width * height)`.
- Memoizing the `capturable_neighbors_of` function yields a 50% speed boost by decreasing the number of calls from
3587 to 600 (once per grid cell). The files `profile-without-memoize.txt` and `profile-with-memoize.txt` provide
a comparison of time performance before and after the memoizing was implemented.
