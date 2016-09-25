"""Support routines for checkio."""
# vim:ts=4:sw=4:tw=0:wm=0:et

from __future__ import print_function
from pprint import pprint


def sprint(s, rows, cols):
    result = []
    for row in range(rows):
        out = ""
        for col in range(cols):
            out += "%d" % s[row][col]
        print(out)
        result.append(out)
    print()
    return result


def treeprint(d, rows, cols):
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


def verify(s, tree, rows, cols):
    r1 = " ".join(sprint(s, rows, cols))
    r2 = " ".join(treeprint(tree, rows, cols))
    print(r1)
    print(r2)
    out = ""
    for i in range(len(r1)):
        out += (" " if r1[i] == r2[i] else "^")
    print(out)
    pprint(s)

# end of file
