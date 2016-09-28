#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

from __future__ import print_function

# Created:       Tue 27 Sep 2016 07:03:30 PM CDT
# Last Modified: Tue 27 Sep 2016 07:27:03 PM CDT


def traverse(start, end, blist, tree, plat):

    loc = start
    level = 0
    stack = [(loc, True)]

    while stack:
        newstack = []
        loc, burdened = stack.pop()
        level += (2 if burdened else 1)

        while loc != end:
            print(loc)
            r, c = loc
            for choice in tree[loc]:
                r0, c0 = choice
                cell_contents = plat[r0][c0]
                print(r0, c0, cell_contents)

                if cell_contents == '-':
                    plat[r0][c0] = level
                    newstack.append(((r0, c0), burdened))

                if cell_contents == 'B':
                    plat[r0][c0] = level
                    newstack.append(((r0, c0), False)

#               if cell_contents == 'W':
#                   pass

#               if cell_contents == 'S':
#                   pass

#               if cell_contents == 'E':
#                   loc = end

    return "RRRDDD"

########################################################################

if __name__ == "__main__":

    start = (0, 0)
    end = (3, 3)
    blist = [(2, 0), (2, 3)]
    tree = {
        (0, 0): set([(0, 1), (1, 0)]),
        (0, 1): set([(0, 0), (0, 2), (1, 1)]),
        (0, 2): set([(0, 1), (0, 3), (1, 2)]),
        (0, 3): set([(0, 2), (1, 3)]),
        (1, 0): set([(0, 0), (1, 1)]),
        (1, 1): set([(0, 1), (1, 0), (1, 2), (2, 1)]),
        (1, 2): set([(0, 2), (1, 1), (1, 3)]),
        (1, 3): set([(0, 3), (1, 2)]),
        (2, 0): set([]),
        (2, 1): set([(1, 1), (3, 1)]),
        (2, 2): set([]),
        (2, 3): set([]),
        (3, 0): set([(3, 1)]),
        (3, 1): set([(2, 1), (3, 0)]),
        (3, 2): set([]),
        (3, 3): set([])
    }
    plat = ["S...", "....", "B.WB", "..WE"]
    traverse(start, end, blist, tree, plat)

########################################################################
