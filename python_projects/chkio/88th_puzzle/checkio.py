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

from heapq import heappush, heappop

########################################################################

DEBUG = False

########################################################################

RINGS_TUPLE = (
    (0, (0, 3, 5, 2)),                  # starting at 'north' going clockwise
    (1, (1, 4, 6, 3)),
    (2, (5, 8, 10, 7)),
    (3, (6, 9, 11, 8))
)

########################################################################


def rotate(t, ring_plus_1):
    """Rotate the 'ring_plus_1' circle by 90 degrees."""
    indices = RINGS_TUPLE[ring_plus_1 - 1][1]
    a, b, c, d = [t[x] for x in indices]

    t2 = list(t)
    for index, t_index in enumerate(indices):
        t2[t_index] = [d, a, b, c][index]

    return t2

########################################################################

VERIFY_LIST = [
    (0, "gray", (3, 5, 6, 8)),
    (1, "blue", (0, 2)),
    (2, "green", (1, 4)),
    (3, "red", (7, 10)),
    (4, "orange", (9, 11))
]

########################################################################


def count_incorrect(t):
    """Count the number of incorrect colors."""
    color_is_correct = []
    for color_index, color_name, locations in VERIFY_LIST:
        for location in locations:
            color_is_correct.append(color_index == t[location])
    return color_is_correct.count(False)

########################################################################


def run_puzzle(t0, path, heap):
    """Try one twist on each circle; pick the best result."""
    t1 = rotate(t0, 1)
    c1 = count_incorrect(t1)
    heappush(heap, (c1, path + "1", t1))

    t2 = rotate(t0, 2)
    c2 = count_incorrect(t2)
    heappush(heap, (c2, path + "2", t2))

    t3 = rotate(t0, 3)
    c3 = count_incorrect(t3)
    heappush(heap, (c3, path + "3", t3))

    t4 = rotate(t0, 4)
    c4 = count_incorrect(t4)
    heappush(heap, (c4, path + "4", t4))

    if DEBUG:
        print("c1", c1, "c2", c2, "c3", c3, "c4", c4, "\n")

########################################################################


def puzzle88(t):
    """Solve the rings puzzle."""

    if DEBUG:
        print(80 * "#")
        print("\npuzzle88\n")
        print(80 * "#")
        print()

    # set up solutions heapsort
    old_heap = []
    path = ""
    c0 = 24
    heappush(old_heap, (c0, path, t))

    # set up fail-safe exit
    loopcount = 0
    MAX_LOOPS = 99999

    while loopcount < MAX_LOOPS and (c0 != 0):

        # new heap to be built from the current heap
        new_heap = []

        # process the old heap
        while old_heap:

            loopcount += 1

            c0, path, t0 = heappop(old_heap)

            if DEBUG:
                print("c0", c0, "path", path, "t0", t0)

            # if count is 0, a solution has been found
            if c0 == 0:
                break

            # run the puzzle turning each circle once
            run_puzzle(t0, path, new_heap)

        # transfer the new heap to the old heap
        old_heap = new_heap

    # show the accumulated path
    if DEBUG:
        print("\npath", path)

    return path

########################################################################

if __name__ == "__main__":

#   assert puzzle88((0, 2, 1, 3, 2, 1, 4, 0, 0, 4, 0, 3)) == "1433"

#   assert puzzle88(
#       (0, 2, 1, 2, 0, 0, 4, 1, 0, 4, 3, 3)
#   ) in ('4231', '4321'), "Rotate all"

#   assert puzzle88(
#       (0, 2, 1, 2, 4, 0, 0, 1, 3, 4, 3, 0)
#   ) in ('2314', '2341', '3214', '3241'), "Four paths"

    assert puzzle88(
        (1, 0, 0, 1, 0, 2, 4, 0, 2, 4, 3, 3)
    ) == "1114223", "Extra credit"

    print("Done!")

# end of file
