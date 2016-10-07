# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/weak-point/

from __future__ import print_function

########################################################################


def weak_point(l):
    row_sums = [sum(x) for x in l]
    col_sums = [sum(y) for y in zip(*l)]
    rmin = min(row_sums)
    r = row_sums.index(rmin)
    cmin = min(col_sums)
    c = col_sums.index(cmin)
    return [r, c]

########################################################################

assert weak_point([[7, 2, 7, 2, 8],
                   [2, 9, 4, 1, 7],
                   [3, 8, 6, 2, 4],
                   [2, 5, 2, 9, 1],
                   [6, 6, 5, 4, 5]]) == [3, 3]

assert weak_point([[7, 2, 4, 2, 8],
                   [2, 8, 1, 1, 7],
                   [3, 8, 6, 2, 4],
                   [2, 5, 2, 9, 1],
                   [6, 6, 5, 4, 5]]) == [1, 2]

print("Done!")

# end of file
