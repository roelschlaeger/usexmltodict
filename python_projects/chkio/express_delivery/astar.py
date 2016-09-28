#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 28 Sep 2016 01:02:02 PM CDT
# Last Modified: Wed 28 Sep 2016 04:06:36 PM CDT

#####################
# Original Citation #
#####################
# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

####################
# Current Citation #
####################
# Author: Robert Oelschlaeger (roelsch2009@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

from __future__ import print_function

import numpy
from heapq import heappush, heappop

"""Neighbors of a given cell"""
NEIGHBORS = [
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
    # (-1, -1),  # diagonal moves from the center square
    # (-1, 1),
    # (1, -1),
    # (1, 1),
]


# Linear distance heuristic
# def heuristic(a, b):
#     return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

# Manhattan distance heuristic
def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def astar(array, start, goal):

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in NEIGHBORS:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and \
                    tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or \
                    neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + \
                    heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return False

if __name__ == "__main__":

    '''Here is an example of using my algo with a numpy array,
    astar(array, start, destination)
    astar function returns a list of points (shortest path)'''

    nmap = numpy.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    print(astar(nmap, (0, 0), (10, 13)))

    # end of file
