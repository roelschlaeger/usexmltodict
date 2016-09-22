"""Solve a maze."""
# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/open-labyrinth/
# https://en.wikipedia.org/wiki/Maze_solving_algorithm#Recursive_algorithm
# http://stackoverflow.com/questions/3097556/programming-theory-solve-a-maze

from __future__ import print_function
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

    tree = {}
    import copy
    s2 = copy.copy(s)
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            l = []
            s2[r][c] = 2
            for dir, ro, co in DIRECTIONS:
                if s2[r+ro][c+co] == 0:
                    l.append((r+ro, c+co))
            if l:
                tree[(r, c)] = l

    def treeprint(d):
        for r in range(rows):
            out = ""
            for c in range(cols):
                if (r, c) in d:
                    out += "0"
                else:
                    out += "1"
            print(out)
        print()

    treeprint(tree)
    pprint(tree)

    if (0):
        stack = [(1, 1, [], s)]

        while stack:
            r, c, l, s = stack.pop()
            s[r][c] = 2  # mark location as having been visited
            for direction, ro, co in DIRECTIONS:
                if s[r+ro][c+co] == 0:
                    l.append((r+ro, c+co, s))
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
