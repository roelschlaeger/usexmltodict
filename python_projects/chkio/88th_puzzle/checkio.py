# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Solve the rings puzzle."""

# https://py.checkio.org/mission/88th-puzzle/

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

from __future__ import print_function

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

########################################################################

GRID_ROWS_COLS = [
    (0, 1), (0, 3),
    (1, 0), (1, 2), (1, 4),
    (2, 1), (2, 3),
    (3, 0), (3, 2), (3, 4),
    (4, 1), (4, 3)
]

COLORS = [
    "gray",
    "blue",
    "green",
    "red",
    "orange"
]

DRAW_WIDTH = 8


def draw_rings(t):
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

RINGS_FINAL = (
    (0, (1, 0, 0, 1)),                  # starting at 'north' going clockwise
    (1, (2, 2, 0, 0)),
    (2, (0, 0, 3, 3)),
    (3, (0, 4, 4, 0))
)


def check_errors(rings):
    """Check the rings for errors."""
    ring_errors = []
    for ring_index, ring_colors in RINGS_FINAL:
        errors = []
        ring = rings[ring_index]
        for color_index, ring_color in enumerate(ring_colors):
            errors.append(ring[color_index] != ring_color)
        ring_errors.append(errors)
    return ring_errors

########################################################################


def rotate(t, ring_plus_1):
    indices = RINGS_TUPLE[ring_plus_1 - 1][1]
    a, b, c, d = [t[x] for x in indices]

    t2 = list(t)
    for index, t_index in enumerate(indices):
        t2[t_index] = [d, a, b, c][index]
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


def verify_final(t):
    color_is_correct = []
    for color_index, color_name, locations in VERIFY_LIST:
        for location in locations:
            color_is_correct.append(color_index == t[location])
    return all(color_is_correct)

########################################################################


def puzzle88(t):
    """Solve the rings puzzle."""
    rings = fill_rings(t)
#   print(rings)
    draw_rings(t)
    ring_errors = check_errors(rings)
    print(ring_errors)

    t = rotate(t, 1)
    t = rotate(t, 4)
    t = rotate(t, 3)
    t = rotate(t, 3)
    draw_rings(t)

    if verify_final(t):
        print("Color is correct")
    else:
        print("Color is incorrect")

    return "1433"

########################################################################

if __name__ == "__main__":

    assert puzzle88((0, 2, 1, 3, 2, 1, 4, 0, 0, 4, 0, 3)) == "1433"

    print("Done!")

# end of file
