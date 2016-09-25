"""Solve a maze."""
# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/open-labyrinth/
# https://en.wikipedia.org/wiki/Maze_solving_algorithm#Recursive_algorithm
# http://stackoverflow.com/questions/3097556/programming-theory-solve-a-maze

from __future__ import print_function
from pprint import pprint
# from support import sprint, treeprint, verify
# from support import treeprint

DIRECTIONS = [
    ("E", 0, 1),
    ("S", 1, 0),
    ("W", 0, -1),
    ("N", -1, 0),
]


def make_tree(s, rows, cols):
    """Recursively solve the maze in s."""

    next = []
    tree = {}
    visited = []


    # push starting location
    next.append((1, 1))

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            tree[(row, col)] = set()

    while next:
        # pop last fork location
        r, c = next.pop()
        visited.append((r, c))
        l = []
#       print_flag = False and (r == 5) and (c == 8)
        for dir, roffset, coffset in DIRECTIONS:
            r2, c2 = r + roffset, c + coffset
#           if print_flag:
#               print("***", r2, c2, tree.get((r2, c2), []), s[r2][c2])
            # available?
            if s[r2][c2] == 0:
                # visited?
                if (r2, c2) not in visited:
                    tree[r, c].add((r2, c2))
                    tree[r2, c2].add((r, c))
#                   l.append((r2, c2))
                    next.append((r2, c2))
#       tree[(r, c)] = l
#       print((r, c), l)

    return tree


def traverse(tree, start, end):

    print()
    print("traverse")
    r0, c0 = start
    r1, c1 = end

    stack = []
    stack.append((start, tree[start]))
#   print(stack)
    print()

    while stack:
        # get current location
        loc, l = stack.pop(0)
        print("%s: %s" % (loc, l))

        if loc == end:
            print("Done!")
            break

        elif l:
            newloc = l.pop()
            stack.append((loc, l))
            stack.append((newloc, tree[newloc]))

        elif stack:
            loc, l = stack.pop(0)

        else:
            raise ValueError("I give up")


def checkio(s):
    rows = len(s)
    cols = len(s[0])
    tree = make_tree(s, rows, cols)
    pprint(tree)
#   treeprint(tree)
#   verify(s, tree, rows, cols)
    traverse(tree, (1, 1), (10, 10))

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
