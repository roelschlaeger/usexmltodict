"""Solve a maze."""
# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/open-labyrinth/
# http://www.dsalgo.com/2013/02/find-shortest-path-in-maze.html

from __future__ import print_function

START = (1, 1)

END = (10, 10)

DIRECTIONS = [
    ("E", 0, 1),
    ("S", 1, 0),
    ("W", 0, -1),
    ("N", -1, 0),
]


def make_tree(s, rows, cols):
    """Recursively solve the maze in s."""

    index = 2
    r, c = START
    s[r][c] = index
    new_frontier = [START]

    index += 1

    while True:
        frontier = new_frontier
        new_frontier = []
        while frontier:
            r0, c0 = frontier.pop()
            for d, roffset, coffset in DIRECTIONS:
                r1, c1 = r0 + roffset, c0 + coffset
                if s[r1][c1] == 0:
                    new_frontier.append((r1, c1))
                    s[r1][c1] = index
                    if (r1, c1) == END:
                        frontier = []
                        new_frontier = []
                        break
        if not new_frontier:
            break
        index += 1

    return s, index


def opposite(d):
    """Return opposite direction."""
    return {
        'N': 'S',
        'E': 'W',
        'S': 'N',
        'W': 'E'
    }[d]


def traverse(s, index):
    """Traverse a path back from the end to the beginning."""

    r0, c0 = END
    path = []

    while (r0, c0) != START:
        index -= 1
        for d, roffset, coffset in DIRECTIONS:
            r1, c1 = r0 + roffset, c0 + coffset
            if s[r1][c1] == index:
                path.insert(0, (r1, c1, opposite(d)))
                r0, c0 = r1, c1
                break
    return path


def checkio(s):
    """Return the path through the maze."""
    rows = len(s)
    cols = len(s[0])

    s2, index = make_tree(s, rows, cols)

    result = traverse(s2, index)

    return [d for (r, c, d) in result]

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
