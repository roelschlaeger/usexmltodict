# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

#

from __future__ import print_function
from itertools import product
# from collections import Counter

########################################################################


def line(p1, p2):
    # put points in ascending X order
    if p1[0] > p2[0]:
        p1, p2 = p2, p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        m = 100
        b = x1
    else:
        # y = mx + b
        m = (y2 - y1) / float(x2 - x1)

        if m != 0:
            if x1 != 0:
                b = y1 / (m * x1)
            else:
                b = y2 / (m * x2)
        else:
            b = y1

    m = round(m, 2)
    b = round(b, 2)
    print("line", p1, p2, m, b)
    return m, b

########################################################################


def print_group(g):
    for l, point_slope, point_list in g:
        print(l, point_slope, point_list)

########################################################################


def checkio(l):
    print("checkio", l)
    counts = {}
    p = product(l, l)
    for p1, p2 in p:
        if p1 == p2 or p1[0] > p2[0]:
            continue
        m, b = line(p1, p2)
        counts.setdefault((m, b), [])
        counts[(m, b)].append((p1, p2))

    datatuples = []
    print("----")
    for k in sorted(counts.keys()):
        print(len(counts[k]), k, counts[k])
        datatuples.append((len(counts[k]), k, counts[k]))

    groups = []
    uniquekeys = []
    data = sorted(datatuples, key=lambda v: v[0])

    from itertools import groupby
    for k, g in groupby(data, lambda v: v[0]):
        groups.append(list(g))
        uniquekeys.append(k)

    # in place reversal
    groups.reverse()
    uniquekeys.reverse()

    print("=====")
    print("groups")
    for group in groups:
        print_group(group)
    print("uniquekeys", uniquekeys)

    all_coverage = set([(x, y) for [x, y] in l])
    print(all_coverage)

    current_coverage = set()
    for group in groups:
        print()
        new_coverage = set()
        for element in group:
            length, slope_intercept, point_list = element
            print(length, slope_intercept, point_list)
            for p1, p2 in point_list:
                x1, y1 = p1
                x2, y2 = p2
                new_coverage.add((x1, y1))
                new_coverage.add((x2, y2))
        print("new_coverage", new_coverage)
        current_coverage |= new_coverage
        print("still missing", all_coverage - current_coverage)




    return counts

########################################################################

checkio([[3, 3], [5, 5], [8, 8], [2, 8], [8, 2]]) == 2
checkio([[2, 2], [2, 5], [2, 8], [5, 2], [7, 2], [8, 2], [9, 2], [4, 5], [4, 8], [7, 5], [5, 8], [9, 8]]) == 6

# end of file
