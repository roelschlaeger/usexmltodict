# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/numbered-triangles/

from __future__ import print_function

########################################################################

from itertools import product, permutations

########################################################################


def rotate(s, n):
    """Return one of the six rotations of the tile."""
    a, b, c = s
    if n == 0:
        return (a, b, c)
    elif n == 1:
        return (b, c, a)
    elif n == 2:
        return (c, a, b)
    elif n == 3:
        return (a, c, b)
    elif n == 4:
        return (c, b, a)
    elif n == 5:
        return (b, a, c)
    else:
        raise ValueError("impossible value for n: %s" % n)

########################################################################


def adjacencies(triangles):
    """Look for matching sides in some permutation of the triangles."""
    # check all tile permutations
    for subscripts in permutations(range(6), 6):

        # extend the permutation to repeate the first node
        ls = list(subscripts)
        ls.append(subscripts[0])

        # check adjacent node values for equality
        nodes_match = True

        # all six tiles
        for index in range(6):
            i = ls[index]
            j = ls[index + 1]

            # right edge of the first matches the left edge of the second
            if triangles[i][0] != triangles[j][1]:
                nodes_match = False
                break

        # success!
        if nodes_match:
            return True

    return False

########################################################################


def checkio(l):
    # start the triangles in a known order: bottom side is subscript 2
    for s in l:
        s.sort()

    # enumerate all possible triangle rotations
    choices = list(product(range(6), repeat=6))

    # no score yet
    max_score = 0

    # take a choice
    for choice in choices:

        # make a list of triangles
        triangles = []
        for index, n in enumerate(choice):
            triangles.append(rotate(l[index], n))

        # check for gross edge matchup requirement
        e0 = sorted([x[0] for x in triangles])
        e1 = sorted([x[1] for x in triangles])
        if e0 != e1:
            continue

        # refine the edge match requirement
        if adjacencies(triangles):

            # compute the outward-facing sum
            total = sum([x[2] for x in triangles])

            # keep the high score
            if total > max_score:
                max_score = total

    return max_score

########################################################################

if __name__ == "__main__":

    if 1:
        assert checkio(
            [
                [1, 4, 20],
                [3, 1, 5],
                [50, 2, 3],
                [5, 2, 7],
                [7, 5, 20],
                [4, 7, 50]
            ]
        ) == 152

        assert checkio(
            [
                [1, 10, 2],
                [2, 20, 3],
                [3, 30, 4],
                [4, 40, 5],
                [5, 50, 6],
                [6, 60, 1]
            ]
        ) == 210

        assert checkio(
            [
                [1, 2, 3],
                [2, 1, 3],
                [4, 5, 6],
                [6, 5, 4],
                [5, 1, 2],
                [6, 4, 3]
            ]
        ) == 21

    assert checkio(
        [
            [5, 9, 5],
            [9, 6, 9],
            [6, 7, 6],
            [7, 8, 7],
            [8, 1, 8],
            [1, 2, 1]
        ]
    ) == 0

    print("Done!")

# end of file
