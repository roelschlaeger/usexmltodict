# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

# https://py.checkio.org/mission/family-gifts/

########################################################################

from __future__ import print_function

########################################################################

from collections import defaultdict
from pprint import pformat
from string import uppercase

########################################################################

N = 8

########################################################################


def couples_gen(nodes):
    """Generate a list of 'couples' chosen from pairs of 'node' members."""
    couples_list = []
    for i in range((len(nodes) // 2) + 1):
        couples_list.append(
            [tuple(nodes[2 * j: 2 * j + 2]) for j in range(i)]
        )
    return couples_list

########################################################################


def compute_adjacency(nodes):
    """Compute the adjacency matrix for 'nodes'."""
    adjacency = defaultdict(list)
    # 'me' is adjacent to everyone else, except self
    for me in nodes:
        others = nodes[:]
        others.remove(me)
        adjacency[me] = others
    # turn into ordinary dictionary
    adjacency = dict(adjacency)
    return adjacency


########################################################################


def adj_to_table(nodes, adj):
    """Generate the required adjacency output format."""
    print(len(nodes))
    for node in nodes:
        t = tuple(adj[node])
        for node2 in nodes:
            print('1' if node2 in t else '0', end=" ")
        print()
    print()

########################################################################


def graph_gen(n):
    """Generate adjacency tables for nodes with 'n' members."""
    # name the nodes 'A' through ....
    nodes = list(uppercase[:n])
    print('# nodes', nodes)

    couples_list_list = couples_gen(nodes)
    print("# couples_list_list", pformat(couples_list_list, width=80))

    for couples_list in couples_list_list:
        adj = compute_adjacency(nodes)
        print("# couples_list", couples_list)
        if couples_list:
            for couples in couples_list:
                x, y = couples
                adj[x].remove(y)
                adj[y].remove(x)
        print("#", "\n# ".join(pformat(adj, width=80).split("\n")))
        print()
        adj_to_table(nodes, adj)

########################################################################

# Generate all graphs for N nodes
for N in range(3, 12 + 1):
    graph_gen(N)

# end of file
