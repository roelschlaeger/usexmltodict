#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 18 Oct 2016 11:59:38 AM CDT
# Last Modified: Tue 18 Oct 2016 12:01:24 PM CDT

"""Print rings for 88th_puzzle."""

########################################################################

GRID_ROWS_COLS = [                      # table for print_rings
    (0, 1), (0, 3),
    (1, 0), (1, 2), (1, 4),
    (2, 1), (2, 3),
    (3, 0), (3, 2), (3, 4),
    (4, 1), (4, 3)
]

########################################################################

COLORS = [                              # colors for print_rings
    "gray",
    "blue",
    "green",
    "red",
    "orange"
]

########################################################################

DRAW_WIDTH = 8                          # width for print_rings

########################################################################

def print_rings(t):
    """Display the rings."""

    output = []

    from collections import defaultdict
    for row in range(5):
        output.append(defaultdict(str))

    for index, color in enumerate(t):
        row, col = GRID_ROWS_COLS[index]
        print(index, color, row, col)
        output[row][col] = COLORS[color].center(DRAW_WIDTH)

    # fill in ring numbers
    ring = 1
    for row in (1, 3):
        for col in (1, 3):
            output[row][col] = ("%s" % ring).center(DRAW_WIDTH)
            ring += 1

    # draw the output
    print(54 * '-')
    for row in range(5):
        for col in range(5):
            print("%8s" % output[row][col], end=" | ")
        print()
        print(54 * '-')
    print()

########################################################################
