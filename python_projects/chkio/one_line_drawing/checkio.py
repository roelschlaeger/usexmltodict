# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Draw a graph with 'lifting the pen'.

In this case, nodes may be repeated but a given edge may be traversed only
once.
"""

# https://py.checkio.org/mission/one-line-drawing/

# dijkstra_search taken from
# http://www.redblobgames.com/pathfinding/a-star/implementation.html

from __future__ import print_function

########################################################################

from pprint import pprint, pformat
import heapq
from collections import defaultdict

########################################################################

DEBUG = True

########################################################################


def debug_print(*a, **b):
    """Debug-only printing"""
    if DEBUG:
        print(*a, **b)


########################################################################


class SimpleGraph:
    """Class to describe the graph."""

    def __init__(self, l):
        """Initialize the SimpleGraph class."""
        self.edges = defaultdict(set)
        self.l = l

    def neighbors(self, id):
        """Return the list of neighbors for node 'id'."""
        return self.edges[id]

    def cost(self, current, next):
        """Return the cost to traverse the (current, next) edge."""
        return 1

    def __str__(self):
        """Support display of the SimpleGraph class."""
        return pformat(self.edges) + "\n" + pformat(self.point_to_points())

    def check_eulerian(self):
        """Determine if a graph is Eulerian.

        A graph is Eulerian iff exactly zero or two vertices are of odd degree,
        all others are even.
        """
        def is_odd(n):
            return (n & 1) == 1

        result = sum([is_odd(len(y)) for (x, y) in self.edges.items()]) \
            in [0, 2]

        debug_print("check_eulerian", self.edges, result)
        return result

    def point_to_points(self):
        result = defaultdict(list)
        nodelist = tuple(sorted(self.edges.keys()))
        print("\n***\nnodelist", nodelist)
        for a, b, c, d in self.l:
            p1 = nodelist.index((a, b))
            p2 = nodelist.index((c, d))
            result[p1].append(p2)
            result[p2].append(p1)
        print("point_to_points", pformat(result))

########################################################################


class PriorityQueue:
    """Wrapper for the heapq data structure."""

    def __init__(self):
        """Initialize the PriorityQueue data element."""
        self.elements = []

    def empty(self):
        """Return 'True' if the data structure is empty."""
        return len(self.elements) == 0

    def put(self, item, priority):
        """Push 'item' onto the queue with 'priority'."""
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """Get the highest priority element."""
        return heapq.heappop(self.elements)[1]

########################################################################


def create_graph(l):
    """Construct a graph and fill in edges."""
    graph = SimpleGraph(l)

    points = []
    for a, b, c, d in l:
        p1 = (a, b)
        p2 = (c, d)
        points.extend([p1, p2])
        graph.neighbors(p1).add(p2)
        graph.neighbors(p2).add(p1)
    points = set(sorted(list(set(points))))
    debug_print("points")
    if DEBUG:
        pprint(points)
    return graph, points

########################################################################


def dijkstra_search(graph, start, goal):
    """Traverse a graph from 'start' to (optional) 'goal'."""
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    edges_so_far = {}
    edges_so_far[start] = []

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            new_edge = tuple(sorted([current, next]))
            if (
                new_edge not in edges_so_far[current] or
                new_cost < cost_so_far[next]
            ):
                #    (
                #        next not in cost_so_far or
                #        new_cost < cost_so_far[next]
                #    ):
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
                edges_so_far[current].append(new_edge)
                if next not in edges_so_far:
                    edges_so_far[next] = []
                edges_so_far[next].append(new_edge)

    return came_from, cost_so_far, edges_so_far

########################################################################


def reconstruct_path(came_from, start, goal):
    """After a path has been found, return the path elements."""
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
#   path.append(start)  # optional
    path.reverse()      # optional
    return path

########################################################################


def draw(l):
    """Draw a graph without lifting the pen."""
    debug_print("\n################################################################")
    graph, points = create_graph(l)
    debug_print(
        "\nl", pformat(l),
        "\npoints", points,
        "\ngraph", str(graph)
    )

    # if the graph is not Eulerian, no path can be found
    if not graph.check_eulerian():
        return tuple()

    path = []
    for start in points:
        came_from, cost_so_far, edges_so_far = \
            dijkstra_search(graph, start, None)
        debug_print(
            "\nstart", start,
            "\ncame_from", pformat(came_from),
            "\ncost_so_far", pformat(cost_so_far),
            "\nedges_so_far", pformat(edges_so_far)
        )
        highest = max(cost_so_far.values())
        if highest != (len(points) - 1):
            continue
        index = cost_so_far.values().index(highest)
        debug_print("index", index, "#points", len(points))
        goal = cost_so_far.keys()[index]
        path = reconstruct_path(came_from, start, goal)
        debug_print("path", path)
    return tuple(path)

########################################################################

if __name__ == "__main__":

    if 0:

        assert draw(
            {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}) == \
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
