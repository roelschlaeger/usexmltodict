# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from pprint import pformat
from collections import defaultdict

########################################################################

DEBUG = True

########################################################################


def make_graph(edges):
    """Create a dictionary of from: [to] from edges."""
    graph = defaultdict(list)
    for from_node, to_node in edges:
        graph[from_node].append(to_node)
    if DEBUG:
        print("make_graph", "\n  graph", pformat(graph))
    return graph

########################################################################


def find_all_paths(graph, start, end, path=[]):
    """Compute all paths in 'graph' from 'start' to 'end'."""
    path = path + [start]

    if start == end:
        return [path]

    if start not in graph:
        return []

    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    if DEBUG:
        print("find_all_paths", "\n  paths", pformat(paths))

    return paths

########################################################################


def n_length_paths(n, graph, start, end):
    """Return paths of length 'n' in 'graph' from 'start' to 'end'."""
    result = [x for x in find_all_paths(graph, start, end) if len(x) == n]
    if DEBUG:
        print("n_length_paths",
              "\n  n", n,
              "\n  start", start,
              "\n  end", end,
              "\n  result", result
              )
    return result

########################################################################


def chains(edges):
    """Compute all chains in the graph defined by 'edges'."""

    # generate the graph
    graph = make_graph(edges)

    # collect all vertex names
    m = sorted(set([x[0] for x in edges] + [x[1] for x in edges]))

    output = []

    # for each possible 'start' vertex
    for start in m:

        # for each actual 'end' vertex
        end_nodes = graph[start]

        # print(
        #     "\nstart", start,
        #     "\nend_nodes", end_nodes
        # )

        result = set()

        for end in end_nodes:
            for path in n_length_paths(len(m), graph, start, end):
                result.add(tuple(path))

        output.append((len(result), start, result))

    return max(output)

########################################################################


def chain_count(s):
    result = chains(s)
    print("\nresult", pformat(result))
    return result[0]

########################################################################

if __name__ == "__main__":

########################################################################

    EDGES = [
        ('Beth', 'Curtis'),
        ('Beth', 'Javier'),
        ('Beth', 'Lee'),
        ('Beth', 'Rachel'),

        ('Curtis', 'Javier'), ('Curtis', 'Rachel'),

        ('Javier', 'Curtis'), ('Javier', 'Lee'),

        ('Lee', 'Javier'), ('Lee', 'Rachel'),

        ('Rachel', 'Curtis'), ('Rachel', 'Lee')
    ]

    EDGES = [
        ('Gary', 'Hollie'),
        ('Hollie', 'Jeanette')
    ]

    result = chain_count(EDGES)

# end of file
