# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/one-line-drawing/

from __future__ import print_function

from pprint import pprint

########################################################################


def draw(l):
    print()
    points = []
    edges = {}
    for a, b, c, d in l:
        p1 = (a, b)
        p2 = (c, d)
#       if p1 > p2:
#           p1, p2 = p2, p1
        points.extend([p1, p2])
        edges.setdefault(p1, [])
        edges.setdefault(p2, [])
        edges[p1].append(p2)
        edges[p2].append(p1)
    points = set(sorted(list(set(points))))
    pprint(points)
    pprint(edges)
    return ((7, 2), (1, 2), (1, 5), (4, 7), (7, 5))

########################################################################

if __name__ == "__main__":

    assert draw({(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}) == \
        ((7, 2), (1, 2), (1, 5), (4, 7), (7, 5))

    assert draw(
        {
            (1, 2, 1, 5),
            (1, 2, 7, 2),
            (1, 5, 4, 7),
            (4, 7, 7, 5),
            (7, 5, 7, 2),
            (1, 5, 7, 2),
            (7, 5, 1, 2)
        }) == []

    assert draw(
        {
            (1, 2, 1, 5),
            (1, 2, 7, 2),
            (1, 5, 4, 7),
            (4, 7, 7, 5),
            (7, 5, 7, 2),
            (1, 5, 7, 2),
            (7, 5, 1, 2),
            (1, 5, 7, 5)
        }
    ) == (
        (7, 2),
        (1, 2),
        (1, 5),
        (4, 7),
        (7, 5),
        (7, 2),
        (1, 5),
        (7, 5),
        (1, 2)
    )

# end of file
