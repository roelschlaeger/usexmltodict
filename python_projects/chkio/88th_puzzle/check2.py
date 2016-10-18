# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

from __future__ import print_function

########################################################################

from itertools import product

PRODUCTS = list(
    product(
        range(1, 5),
        range(1, 5),
        range(1, 5),
        range(1, 5)
    )
)

# remove the back-to-start entries
for q in [(x, x, x, x) for x in range(1, 5)]:
    PRODUCTS.remove(q)

########################################################################

RINGS_TUPLE = (
    (0, (0, 3, 5, 2)),                  # starting at 'north' going clockwise
    (1, (1, 4, 6, 3)),
    (2, (5, 8, 10, 7)),
    (3, (6, 9, 11, 8))
)


def rotate(t, ring_plus_1):
    """Rotate the 'ring_plus_1' circle by 90 degrees."""
    indices = RINGS_TUPLE[ring_plus_1 - 1][1]
    a, b, c, d = [t[x] for x in indices]

    t2 = list(t)
    for index, t_index in enumerate(indices):
        t2[t_index] = [d, a, b, c][index]

#   if DEBUG:
#       print("rotate", t, ring_plus_1, indices, t2)

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


def puzzle88(t):
    """Solve the rings puzzle."""

    # initialize error count and marble configuration

    for p in PRODUCTS:

        # pick a permutation
        d1, d2, d3, d4 = p

        # use the permutation
        t1 = rotate(t, d1)
        c1 = count_incorrect(t1)
        if c1 == 0:
            return "%d" % d1

        t2 = rotate(t1, d2)
        c2 = count_incorrect(t2)
        if c2 == 0:
            return "%d%d" % (d1, d2)

        t3 = rotate(t2, d3)
        c3 = count_incorrect(t3)
        if c3 == 0:
            return "%d%d%d" % (d1, d2, d3)

        t4 = rotate(t3, d4)
        c4 = count_incorrect(t4)

        # check for any success
        if c4 == 0:
            return "%d%d%d%d" % (d1, d2, d3, d4)

    # if normal non-break exit
    else:
        result = "0000"

    return result

########################################################################
print(puzzle88((1, 0, 0, 1, 0, 2, 4, 0, 2, 4, 3, 3)))

assert puzzle88((1, 2, 0, 1, 2, 0, 0, 3, 0, 4, 3, 4)) == "111"

assert puzzle88((0, 2, 1, 3, 2, 1, 4, 0, 0, 4, 0, 3)) == "1433"

assert puzzle88(
    (0, 2, 1, 2, 0, 0, 4, 1, 0, 4, 3, 3)) in ('4231', '4321'), "Rotate all"

assert puzzle88(
    (0, 2, 1, 2, 4, 0, 0, 1, 3, 4, 3, 0)
) in ('2314', '2341', '3214', '3241'), "Four paths"

print("Done!")
