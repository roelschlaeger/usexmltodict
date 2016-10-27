#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 26 Oct 2016 06:15:01 PM CDT
# Last Modified: Wed 26 Oct 2016 07:20:27 PM CDT

from __future__ import print_function

from pprint import pformat
from heapq import heappush, heappop

from p0 import p0


def edges(p1):
    return set(
        [(p1[i], p1[i + 1]) for i in range(len(p1) - 1)] + [(p1[-1], p1[0])]
    )


def pnext(p0):

    # create a work stack
    stack = []

    heappush(stack, (-len(p0), "", p0))

    # while there is work to do
    while stack:

        if len(stack) > 20:
            raise ValueError("Stack too large")

        # pop a job
        remaining, thread, p0 = heappop(stack)
        print(remaining, len(stack), thread, len(p0))

        # get a sample
        p1 = p0.pop(0)
        yes = [p1]
        no = []

        p1_edges = edges(p1)

        # split the remaining samples into groups that are compatible with the
        # current sample
        for p2 in p0:
            # if they share edges, put them into different groups
            if edges(p2).intersection(p1_edges):
                no.append(p2)
            else:
                yes.append(p2)

        ythread = thread + "Y"
        if len(yes) == 1:
            print(ythread, pformat(yes[0]))
        elif len(no) > 0:
            heappush(stack, (-len(yes), ythread, yes))
        else:
            print(ythread, pformat(yes[0]))

        nthread = thread + "N"
        if len(no) > 0:
            heappush(stack, (-len(no), nthread, no))

        print("len(yes)", len(yes), "len(no)", len(no))

pnext(p0)

# end of file
