# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Solve the rings puzzle."""

# https://py.checkio.org/mission/88th-puzzle/

from __future__ import print_function

# ###########################
# # marble location indices #
# ###########################
#
#      0     1
#   2     3     4
#      5     6
#   7     8     9
#     10     11

# #################
# # marble colors #
# #################
#
#   COLOR              LOCATION
#   ##########         ############
#   0 - gray           (3, 5, 6, 8)
#   1 - blue           (0, 2)
#   2 - green          (1, 4)
#   3 - red            (7, 10)
#   4 - orange         (9, 11)
#
# #########
# # rings #
# #########
#
# RING                 LOCATION
# ####                 #############
# 1                    (0, 2, 3, 5)
# 2                    (1, 3, 4, 6)
# 3                    (5, 7, 8, 10)
# 4                    (6, 8, 9, 11)

########################################################################

DEBUG = False

########################################################################

RINGS_TUPLE = (
    (0, (0, 3, 5, 2)),                  # starting at 'north' going clockwise
    (1, (1, 4, 6, 3)),
    (2, (5, 8, 10, 7)),
    (3, (6, 9, 11, 8))
)


def fill_rings(t):
    """Fill the rings with input colors."""
    rings = [[], [], [], []]
    for ring_index, ring_locations in RINGS_TUPLE:
        for t_index in ring_locations:
            rings[ring_index].append(t[t_index])
    return rings

if DEBUG:

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

else:

    def print_rings():
        pass

########################################################################


def rotate(t, ring_plus_1):
    """Rotate the 'ring_plus_1' circle by 90 degrees."""
    indices = RINGS_TUPLE[ring_plus_1 - 1][1]
    a, b, c, d = [t[x] for x in indices]

    t2 = list(t)
    for index, t_index in enumerate(indices):
        t2[t_index] = [d, a, b, c][index]

    if DEBUG:
        print("rotate", t, ring_plus_1, indices, t2)

    return t2

########################################################################


VERIFY_LIST = [
    (0, "gray", (3, 5, 6, 8)),
    (1, "blue", (0, 2)),
    (2, "green", (1, 4)),
    (3, "red", (7, 10)),
    (4, "orange", (9, 11))
]


def count_incorrect(t):
    """Count the number of incorrect colors."""
    color_is_correct = []
    for color_index, color_name, locations in VERIFY_LIST:
        for location in locations:
            color_is_correct.append(color_index == t[location])
    return color_is_correct.count(False)

########################################################################


def run_puzzle(t):
    """Try one twist on each circle; pick the best result."""
    if DEBUG:
        print("run_puzzle", t)

    t1 = rotate(t, 1)
    c1 = count_incorrect(t1)

    t2 = rotate(t, 2)
    c2 = count_incorrect(t2)

    t3 = rotate(t, 3)
    c3 = count_incorrect(t3)

    t4 = rotate(t, 4)
    c4 = count_incorrect(t4)

    if DEBUG:
        print("c1", c1, "c2", c2, "c3", c3, "c4", c4, "\n")

    return min([
        (c1, "1", t1),                  # errors, path, configuration
        (c2, "2", t2),
        (c3, "3", t3),
        (c4, "4", t4),
    ])

########################################################################


def puzzle88(t):
    """Solve the rings puzzle."""

    # start with no path
    path = ""

    # initialize error count and marble configuration
    c0, t0 = (12, t)

    if DEBUG:
        print("c0", c0, "t0", t0)

    for _ in range(24):

        # run the puzzle once on each circle, keeping the best
        c0, p0, t0 = run_puzzle(t0)
        path += p0

        if DEBUG:
            print("c0", c0, "p0", p0, "t0", t0)

        # check for getting done early
        if c0 == 0:
            break

    # show the accumulated path
    if DEBUG:
        print("\npath", path)

    return path

########################################################################

if __name__ == "__main__":

    assert puzzle88((0, 2, 1, 3, 2, 1, 4, 0, 0, 4, 0, 3)) == "1433"

    print("Done!")

# end of file
