"""Solve a maze."""
# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/open-labyrinth/
# https://en.wikipedia.org/wiki/Maze_solving_algorithm#Recursive_algorithm
# http://stackoverflow.com/questions/3097556/programming-theory-solve-a-maze

from __future__ import print_function
import copy
from pprint import pprint

DIRECTIONS = [
    ("E", 0, 1),
    ("S", 1, 0),
    ("W", 0, -1),
    ("N", -1, 0),
]


def checkio(s):
    """Recursively solve the maze in s."""
    rows = len(s)
    cols = len(s[0])

    next = []
    tree = {}

    s2 = copy.copy(s)
    next.append((1, 1))

    while next:
        r, c = next.pop(0)
        l = []
        for dir, roffset, coffset in DIRECTIONS:
            r2, c2 = r + roffset, c + coffset
            # already visited?
            if not (r2, c2) in tree:
                # available?
                if s2[r2][c2] == 0:
                    l.append((r2, c2))
                    next.append((r2, c2))
        tree[(r, c)] = l
        print((r, c), l)

    def sprint(s):
        result = []
        for row in range(rows):
            out = ""
            for col in range(cols):
                out += "%d" % s[row][col]
            print(out)
            result.append(out)
        print()
        return result

    def treeprint(d):
        result = []
        for r in range(rows):
            out = ""
            for c in range(cols):
                if (r, c) in d:
                    out += "0"
                else:
                    out += "1"
            print(out)
            result.append(out)
        print()
        return result

    r1 = " ".join(sprint(s))
    r2 = " ".join(treeprint(tree))
    print(r1)
    print(r2)
    out = ""
    for i in range(len(r1)):
        out += (" " if r1[i] == r2[i] else "^")
    print(out)
    pprint(s)

#   pprint(tree)

    if (0):
        stack = [(1, 1, [], s)]

        while stack:
            r, c, l, s = stack.pop()
            s[r][c] = 2  # mark location as having been visited
            for direction, ro, co in DIRECTIONS:
                if s[r + ro][c + co] == 0:
                    l.append((r + ro, c + co, s))
            break

        pprint(stack)
        pprint(s)
        pprint(l)

checkio([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
