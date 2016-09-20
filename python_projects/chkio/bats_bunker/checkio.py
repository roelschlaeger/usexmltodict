# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

from __future__ import print_function

# https://py.checkio.org/mission/bats-bunker/

"""Compute the minimum distance to the Alpha bat in the bat bunker"""

"""
You are given the map of bunker as a list of strings:
"-" is an empty cell
"W" is a wall
"B" is a bat
"A" is the Alpha Bat

The entrance is placed at top left cell and there's always a bat right there
(be careful, the Alpha bat can be here too).

You should calculate the minimal possible time for the alert to reach the
leader with a precision of two digits (±0.01).
"""


def checkio(s):
    """Compute the minimum distance to the Alpha bat in the bat bunker."""
    rows = len(s)
    cols = len(s[0])
    print(rows, cols)

    out = []
    for col_string in s:
        out.append(list(col_string))
    s = out

    assert s[0][0] == "B" or s[0][0] == "A"

    pathlists = [
        (s, (0, 0), 0, [])
    ]

    row = 0
    col = 0
    left = 0
    start = (0, 0)
    length = 0
    visited = []

    def check(r, c):
        # check for out of bounds
        if (r < 0) or (r > rows) or (c < 0) or (c > cols):
            return

        if s[r][c] == "V":  # already visited
            pass
        elif s[r][c] == "-":  # empty
            s[r][c] = "V"  # mark as visited
            visited.append((r, c))
            pathlists.append((left, start, length, visited))
        elif s[r][c] == "W":  # wall
            pass
        elif s[r][c] == "A":  # alpha bat
            pass
        elif s[r][c] == "B":  # another bat
            s[r][c] = "V"  # visited
            visited.append((r, c))
            pathlists.append((left, start, length, visited))
        else:
            print("Unexpected character at %d %d: '%c'" % (r, c, s[r][c]))

    for pathlist in pathlists:
        left, start, length, visited = pathlist
        print(left, start, visited)

        row, col = start
        check(row - 1, col - 1)
        check(row - 1, col)
        check(row - 1, col + 1)
        check(row, col - 1)
        check(row, col + 1)
        check(row + 1, col - 1)
        check(row + 1, col)
        check(row + 1, col + 1)

    return 0

assert checkio([
    "B--",
    "---",
    "--A"]) == 2.83
assert checkio([
    "B-B",
    "BW-",
    "-BA"]) == 4
assert checkio([
    "BWB--B",
    "-W-WW-",
    "B-BWAB"]) == 12
assert checkio([
    "B---B-",
    "-WWW-B",
    "-WA--B",
    "-W-B--",
    "-WWW-B",
    "B-BWB-"]) == 9.24
