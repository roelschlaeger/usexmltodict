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
    couples_list = []
    for i in range(len(nodes) // 2):
        couples_list.append(
            [tuple(nodes[2 * j: 2 * j + 2]) for j in range(i)]
        )
    return couples_list

########################################################################


def compute_adjacency(nodes):
    adjacency = defaultdict(list)
    for me in nodes:
        others = nodes[:]
        others.remove(me)
        adjacency[me] = others
    adjacency = dict(adjacency)
    return adjacency


########################################################################


def adj_to_table(nodes, adj):
    pass
    print(len(nodes))
    for node in nodes:
        t = tuple(adj[node])
        for node2 in nodes:
            print('1' if node2 in t else '0', end=" ")
        print()
    print()

########################################################################


def graph_gen(N):

    nodes = list(uppercase[:N])
    print(nodes)

    couples_list_list = couples_gen(nodes)
    print("couples_list_list", pformat(couples_list_list))

    for couples_list in couples_list_list:
        adj = compute_adjacency(nodes)
        print("couples_list", couples_list)
        if couples_list:
            for couples in couples_list:
                x, y = couples
                adj[x].remove(y)
                adj[y].remove(x)
        print(adj)
        adj_to_table(nodes, adj)

########################################################################

graph_gen(N)

# end of file
