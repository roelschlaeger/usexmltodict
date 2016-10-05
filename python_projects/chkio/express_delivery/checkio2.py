# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/express-delivery/

"""
                        Compute Express Delivery Route.

Our three robots found a few mysterious boxes on the island. After some
examination Nicola discovered that these boxes have an an interesting feature.
If you place something in one of them, you can retrieve it again from any other
box. Stephan figures this makes for quick delivery of cargo across the island,
moving loads twice as fast. Stephan can place the cargo in one box and pick it
up later at the delivery point. On the map there are water cells which Stephan
can't pass, but else these boxes will make his task a whole lot easier.

The map for delivery is presented as an array of strings, where:

    "W" is a water (closed cell)
    "B" is a box
    "E" is a goal point.
    "S" is a start point.
    "." is an empty cell.

Stephan moves between neighbouring cells in two minutes if he carries a load.
Without any carry-on luggage, he only needs one minute. Loading and unloading
of cargo in (and out of) the box takes one minute. You should find the fastest
way for the cargo delivery (minimum time).

The route is a string, where each letter is an action.

    "U" -- Up (north)
    "D" -- Down (south)
    "L" -- Left (west)
    "R" -- Right (east)
    "B" -- Load or unload in (out) a box.

"""

from __future__ import print_function
from pprint import pprint, pformat
from numpy import array
from astar import astar
from find_path import find_path

########################################################################

DIRECTIONS = [
    ("U", -1, 0),
    ("D", 1, 0),
    ("L", 0, -1),
    ("R", 0, 1),
]

########################################################################


def compute_steps(plat):
    table = {}
    rows = len(plat)
    cols = len(plat[0])

    for row in range(rows):
        for col in range(cols):
            for dir, roffset, coffset in DIRECTIONS:
                r, c = row + roffset, col + coffset
                if (0 <= r < rows) and (0 <= c < cols):
                    table[(row, col), (r, c)] = dir
    pprint(table)
    return table

########################################################################


def find_points(plat):
    rows = len(plat)
    cols = len(plat[0])

    r0 = c0 = re = ce = -1
    blist = []

    for r in range(rows):

        for c in range(cols):

            v = plat[r][c]

            if v == 'S':
                r0, c0 = r, c

            if v == 'E':
                re, ce = r, c

            if v == 'B':
                blist.append((r, c))

    return (r0, c0), (re, ce), blist

########################################################################


def array_convert(plat, walls):
    """Convert the plat array to a numpy numeric array."""

    print("array_convert")
    pprint(plat)
    pprint(walls)

    rows = len(plat)
    cols = len(plat[0])

    r2 = []

    for row in range(rows):

        c2 = []
        for col in range(cols):
            c = plat[row][col]
            c2.append(1 if c in walls else 0)

        r2.append(c2)

    pprint(r2)
    print()

    return array(r2)

########################################################################


def checkio(plat):
    """Compute Express Delivery Route."""

    print()
    print(72 * '#')
    print("checkio")
    print(72 * '#')

    pprint(plat)
    print()

    # compute direction dictionary for all cell moves
    steps = compute_steps(plat)
    print("steps", pformat(steps))

    start, end, blist = find_points(plat)
    print(start, end, blist)
    print()

    from_start = {}
    to_end = {}
    b_to_b = {}
    aplat = array_convert(plat, 'W')

    # find the direct path from start to end treating bubbles like walls
    direct = astar(aplat, start, end)
    print("direct")
    pprint(direct)

    # now find paths using bubbles
    # for all bubbles
    for b in blist:

        # compute the path from start to bubble
        from_start[(start, b)] = astar(aplat, start, b)
        # compute the path from bubble to end
        to_end[(b, end)] = astar(aplat, b, end)

        # compute the path from bubble to other bubbles
        for b2 in blist:
            # skip current bubble
            if b2 == b:
                continue

            # compute in both directions
            b_to_b[(b, b2)] = astar(aplat, b, b2)
            b_to_b[(b2, b)] = astar(aplat, b2, b)

    print("from_start")
    pprint(from_start, width=32)
    print()

    print("b_to_b")
    pprint(b_to_b, width=32)
    print()

    print("to_end")
    pprint(to_end, width=32)
    print()

    result = find_path(steps, direct, start, end, from_start, b_to_b, to_end)
    print()
    print("checkio result", result)
    return result

########################################################################

assert checkio(["S...", "....", "B.WB", "..WE"]) == "RRRDDD"
assert checkio(["S...", "....", "B..B", "..WE"]) == "DDBRRRBD"
print("Done!")

########################################################################
