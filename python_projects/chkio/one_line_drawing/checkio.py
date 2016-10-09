# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/one-line-drawing/

# dijkstra_search taken from
# http://www.redblobgames.com/pathfinding/a-star/implementation.html

from __future__ import print_function

from pprint import pprint, pformat

########################################################################


class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        if not id in self.edges:
            self.edges[id] = set()
        return self.edges[id]

    def cost(self, current, next):
        return 1

    def __str__(self):
        return pformat(self.edges)

########################################################################

import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

########################################################################


def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

########################################################################


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
#   path.append(start)  # optional
    path.reverse()      # optional
    return path

########################################################################


def create_graph(l):
    graph = SimpleGraph()

    points = []
    for a, b, c, d in l:
        p1 = (a, b)
        p2 = (c, d)
        points.extend([p1, p2])
        graph.neighbors(p1).add(p2)
        graph.neighbors(p2).add(p1)
    points = set(sorted(list(set(points))))
    print("points")
    pprint(points)
    return graph, points

########################################################################


def draw(l):
    print("\n################################################################")
    graph, points = create_graph(l)
    print("graph", graph, "points", points)
    path = []
    for start in points:
        came_from, cost_so_far = dijkstra_search(graph, start, None)
        print(
            "\nstart", start,
            "\ncame_from", came_from,
            "\ncost_so_far", cost_so_far
        )
        highest = max(cost_so_far.values())
        if highest != (len(points) - 1):
            continue
        index = cost_so_far.values().index(highest)
        print("index", index, "#points", len(points))
        goal = cost_so_far.keys()[index]
        path = reconstruct_path(came_from, start, goal)
        print("path", path)
    return tuple(path)

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
        }) == ()

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
        (7, 2), (1, 2), (1, 5), (4, 7), (7, 5), (7, 2), (1, 5), (7, 5), (1, 2)
    )

# end of file
