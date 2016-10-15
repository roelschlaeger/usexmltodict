# vim:ts=4:sw=4:tw=0:wm=0:et

# implementation of Fleury's algorithm
# from https://github.com/DiegoAscanio/python-graphs/blob/master/eulerian.py

from __future__ import print_function

from copy import copy
from collections import defaultdict
from pprint import pformat

'''

    is_connected - Checks if a graph in the form of a dictionary is
    connected or not, using Breadth-First Search Algorithm (BFS)

'''


def is_connected(G):
    start_node = list(G)[0]
    color = {v: 'white' for v in G}
    color[start_node] = 'gray'
    S = [start_node]
    while len(S) != 0:
        u = S.pop()
        for v in G[u]:
            if color[v] == 'white':
                color[v] = 'gray'
                S.append(v)
            color[u] = 'black'
    return list(color.values()).count('black') == len(G)

'''
    odd_degree_nodes - returns a list of all G odd degrees nodes
'''


def odd_degree_nodes(G):
    odd_degree_nodes = []
    for u in G:
        if len(G[u]) % 2 != 0:
            odd_degree_nodes.append(u)
    return odd_degree_nodes

'''
    from_dict - return a list of tuples links from a graph G in a
    dictionary format
'''


def from_dict(G):
    links = []
    for u in G:
        for v in G[u]:
            links.append((u, v))
    return links

'''
    fleury(G) - return eulerian trail from graph G or a
    string 'Not Eulerian Graph' if it's not possible to trail a path
'''


def fleury(G):
    '''
        checks if G has eulerian cycle or trail
    '''
    trail = []
    odn = odd_degree_nodes(G)
    if len(odn) > 2 or len(odn) == 1:
        # print('Not Eulerian Graph')
        pass
    else:
        g = copy(G)
        if len(odn) == 2:
            u = odn[0]
        else:
            u = list(g)[0]
        while len(from_dict(g)) > 0:
            current_vertex = u
            for u in g[current_vertex]:
                g[current_vertex].remove(u)
                g[u].remove(current_vertex)
                bridge = not is_connected(g)
                if bridge:
                    g[current_vertex].append(u)
                    g[u].append(current_vertex)
                else:
                    break
            if bridge:
                g[current_vertex].remove(u)
                g[u].remove(current_vertex)
                g.pop(current_vertex)
            trail.append((current_vertex, u))
    return trail

########################################################################


class FleuryGraph(object):

    def __init__(self, l):
        self.edgelist = None

    def make_graph(self, l):
        nodes = set()
        for a, b, c, d in l:
            p1 = (a, b)
            p2 = (c, d)
            nodes.add(p2)
            nodes.add(p1)

        result = defaultdict(list)
        self.edgelist = tuple(sorted(nodes))
        for a, b, c, d in l:
            p1 = self.edgelist.index((a, b))
            p2 = self.edgelist.index((c, d))
            result[p1].append(p2)
            result[p2].append(p1)
        print("point_to_points", pformat(result))
        return result

    def to_nodes(self, indices):
        print("to_node", indices)
        result = []
        if indices:
            for from_node, to_node in indices:
                result.append(self.edgelist[from_node])
            result.append(self.edgelist[to_node])
            print(
                "to_nodes",
                "\nindices", indices,
                "\nedgelist", self.edgelist,
                "\nresult", result
            )
        return result

########################################################################


def draw(l):
    graph = FleuryGraph(l)
    G = graph.make_graph(l)
    indices = fleury(G)
    result = tuple(graph.to_nodes(indices))
    print("draw", result, "\n*** DONE ***\n\n")
    return result

if __name__ == "__main__":

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

    #   # testing seven bridges of konigsberg
    #   print('Konigsberg')
    #   G = {0: [2, 2, 3], 1: [2, 2, 3], 2: [0, 0, 1, 1, 3], 3: [0, 1, 2]}
    #   print(fleury(G))

    #   # testing an eulerian cycle
    #   print('1st Eulerian Cycle')
    #   G = {
    #       0: [1, 4, 6, 8],
    #       1: [0, 2, 3, 8],
    #       2: [1, 3],
    #       3: [1, 2, 4, 5],
    #       4: [0, 3],
    #       5: [3, 6],
    #       6: [0, 5, 7, 8],
    #       7: [6, 8],
    #       8: [0, 1, 6, 7]
    #   }
    #   print(fleury(G))

    #   # testing another eulerian cycle
    #   print('2nd Eulerian Cycle')
    #   G = {
    #       1: [2, 3, 4, 4],
    #       2: [1, 3, 3, 4],
    #       3: [1, 2, 2, 4],
    #       4: [1, 1, 2, 3]
    #   }
    #   print(fleury(G))

    #   # testing an eulerian trail
    #   print('Eulerian Trail')
    #   G = {1: [2, 3], 2: [1, 3, 4], 3: [1, 2, 4], 4: [2, 3]}
    #   print(fleury(G))


    #   ### assert fleury(
    #   ###     {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}) == \
    #   ###     ((7, 2), (1, 2), (1, 5), (4, 7), (7, 5))
    #   ###
    #   ### assert fleury(
    #   ###     {
    #   ###         (1, 2, 1, 5),
    #   ###         (1, 2, 7, 2),
    #   ###         (1, 5, 4, 7),
    #   ###         (4, 7, 7, 5),
    #   ###         (7, 5, 7, 2),
    #   ###         (1, 5, 7, 2),
    #   ###         (7, 5, 1, 2)
    #   ###     }) == ()
    #   ###
    #   ### assert fleury(
    #   ###     {
    #   ###         (1, 2, 1, 5),
    #   ###         (1, 2, 7, 2),
    #   ###         (1, 5, 4, 7),
    #   ###         (4, 7, 7, 5),
    #   ###         (7, 5, 7, 2),
    #   ###         (1, 5, 7, 2),
    #   ###         (7, 5, 1, 2),
    #   ###         (1, 5, 7, 5)
    #   ###     }
    #   ### ) == (
    #   ###     (7, 2),
    #   ###     (1, 2),
    #   ###     (1, 5),
    #   ###     (4, 7),
    #   ###     (7, 5),
    #   ###     (7, 2),
    #   ###     (1, 5),
    #   ###     (7, 5),
    #   ###     (1, 2)
    #   ### )

    #   G = {
    #       0: [1, 3, 4],
    #       1: [0, 2, 4, 3],
    #       2: [4, 1],
    #       3: [0, 4, 1],
    #       4: [0, 2, 3, 1]
    #   }

    #   print(fleury(G))
