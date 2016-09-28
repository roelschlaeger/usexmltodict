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

########################################################################

DIRECTIONS = [
    ("U", -1, 0),
    ("D", 1, 0),
    ("L", 0, -1),
    ("R", 0, 1),
]

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


def make_tree(plat):
    """Recursively solve the maze in plat."""

    start, end, blist = find_points(plat)

    rows = len(plat)
    cols = len(plat[0])

    next = []
    tree = {}
    visited = []

    # push starting location
    next.append(start)

    for row in range(0, rows):
        for col in range(0, cols):
            tree[(row, col)] = set()

    while next:
        # pop last fork location
        r, c = next.pop()
        visited.append((r, c))

        # for the four cardinal directions
        for dir, roff, coff in DIRECTIONS:

            # compute new coordinates
            r0, c0 = r + roff, c + coff

            # check for still in bounds
            if (r0 < 0) or (r0 >= rows) or (c0 < 0) or (c0 >= cols):
                continue

            # available?
            v = plat[r0][c0]
            if v in ['.']:
                # visited?
                if (r0, c0) not in visited:
                    tree[r, c].add((r0, c0))
                    tree[r0, c0].add((r, c))
                    next.append((r0, c0))
            elif v in ['B']:
                pass
            else:
                pass

    return start, end, blist, tree

########################################################################


def checkio(plat):
    """Compute Express Delivery Route."""

    pprint(plat)
    print()

    start, end, blist, tree = make_tree(plat)
    print(start, end, blist, pformat(tree))
    print()

    return ""

########################################################################

assert checkio(["S...", "....", "B.WB", "..WE"]) == "RRRDDD"
assert checkio(["S...", "....", "B..B", "..WE"]) == "DDBRRRBD"
print("Done!")

########################################################################
