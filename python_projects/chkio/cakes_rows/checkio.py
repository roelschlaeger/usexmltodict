# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

#

from __future__ import print_function

from itertools import product

########################################################################


def line(p1, p2):
    """Compute parameters for 'm' and 'b for y = mx + b line between p1 and
p2."""

    x1, y1 = p1
    x2, y2 = p2

    # avoid division by zero; synthesize fake slope
    if x1 == x2:
        m = 100
        b = x1
    else:
        # y = mx + b
        m = (y2 - y1) / float(x2 - x1)
        b = y1 - (m * x1)

    # sand down the precision a bit
    m = round(m, 2)
    b = round(b, 2)

    # return the line parameters
    return m, b

########################################################################


def checkio(l):
    """Compute colinear groups of points."""

    # start with empty results array
    counts = {}

    # form all pairs of points
    p = product(l, l)

    # work on all point pairs
    for p1, p2 in p:
        # skip equal pairs and take unequal pairs only once
        if (
            (p1 == p2) or
            (p1[0] > p2[0]) or
            ((p1[0] == p2[0]) and (p1[1] > p2[1]))
        ):
            continue

        # compute the line parameters between the points
        m, b = line(p1, p2)

        # accumulate point pairs into a dictionary indexed by (m, b)
        counts.setdefault((m, b), set())
        counts[(m, b)].add(tuple(p1))
        counts[(m, b)].add(tuple(p2))

    # got all of the pairs sorted by line, now keep the lines having three or
    # more points

    datatuples = []
    for k in sorted(counts.keys()):
        if len(counts[k]) >= 3:
            datatuples.append((len(counts[k]), k, counts[k]))

    # whatever lines are left is the answer
    return len(datatuples)

########################################################################

assert checkio([[3, 3], [5, 5], [8, 8], [2, 8], [8, 2]]) == 2
assert checkio([[2, 2], [2, 5], [2, 8], [5, 2], [7, 2], [8, 2], [9, 2], [4, 5], [4, 8], [7, 5], [5, 8], [9, 8]]) == 6
assert checkio([[2, 0], [8, 0], [3, 3], [4, 3], [6, 3], [7, 3], [4, 6], [6, 6], [5, 9]]) == 5
print("Done!")

# end of file
