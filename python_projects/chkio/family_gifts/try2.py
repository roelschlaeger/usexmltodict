# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from collections import defaultdict, deque
from itertools import combinations
from pprint import pformat

########################################################################


# def print_chains(c):
#     edges = sorted(c + [(y, x) for (x, y) in c])
#     c_edges = Counter([x[0] for x in edges])
#     min_c_edges = min(c_edges.values())
#     m = set([x[0] for x in edges])
#
#     pairs = defaultdict(list)
#     for f, t in edges:
#         pairs[f].append(t)
#
#     print("\n  print_chains",
#           "\n    edges", pformat(edges),
#           "\n    c_edges", pformat(c_edges),
#           "\n    min_c_edges", min_c_edges,
#           "\n    m", pformat(m),
#           "\n    pairs", pformat(pairs)
#           )
#
#     chains = []
#
#     print("chains", pformat(chains))

########################################################################


class SimpleGraph:
    def __init__(self, edges={}):
        self.edges = edges

    def neighbors(self, id):
        return self.edges[id]

########################################################################


class Queue(object):

    def __init__(self):
        self.elements = deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

########################################################################


def breadth_first_search(graph, start):

    print("\nbreadth_first_search")

    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    edges_from = defaultdict(list)

    while not frontier.empty():
        current = frontier.get()
        for next in graph.neighbors(current):
            if next not in came_from and \
                    tuple(sorted([current, next])) not in edges_from[current]:
                frontier.put(next)
                came_from[next] = current
                edges_from[current].append(tuple(sorted([current, next])))
                print("\ncurrent", current, "next", next)

    return came_from

########################################################################


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start)                  # optional
    path.reverse()                      # optional
    return path

########################################################################


def build_path(members, edges):
    bidirectional_edges = sorted(edges + [(y, x) for (x, y) in edges])

    neighbors = defaultdict(list)
    for f, t in bidirectional_edges:
        neighbors[f].append(t)
    print("\n\nbuild_path",
          "\nneighbors", pformat(neighbors)
          )

    graph = SimpleGraph(neighbors)

    goal = list(members)[0]
    for start in list(members):
        came_from = breadth_first_search(graph, start)
        print("\ncame_from", pformat(came_from))
        froms = set(came_from.values())
#       tos = set(came_from.keys())
        missing = members - froms
        print(
            "\n",
            "members", members,
            "froms", froms,
            "missing", missing
        )

        if missing == set():
            print("None missing")
            break

    reconstructed_path = reconstruct_path(came_from, start, goal)
    print("\nreconstructed_path ", pformat(reconstructed_path))

    return reconstructed_path

########################################################################


def find_chains(members, married_couples={}):
    # form all the combinations
    edges = list(combinations(sorted(members), 2))

    # remove the couples from the combinations
    for group in married_couples:
        edges.remove(tuple(sorted(group)))

    # display the input
    print("\n\nfind_chains",
          "\n  members", pformat(members),
          "\n  married_couples", pformat(married_couples),
          "\n  edges", pformat(edges)
          )

    path = build_path(members, edges)
    print("path", pformat(path))

    return 0

########################################################################

if 1:

    if 1:

        assert find_chains(
            {'Gary', 'Jeanette', 'Hollie'},
            (
                {'Gary', 'Jeanette'},
            )
        ) == 0  # 0 chains

    assert find_chains(
        {'Curtis', 'Lee', 'Rachel', 'Javier'},
        (
            {'Rachel', 'Javier'},
            {'Curtis', 'Lee'},
        )
    ) == 2  # 2 chains

else:

    assert find_chains(
        {'Beth', 'Curtis', 'Lee', 'Rachel', 'Javier'},
        (
            {'Rachel', 'Javier'},
            {'Curtis', 'Lee'},
        )
    ) == 2  # 2 chains

print("Done!")

# end of file
