# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/digits-doublets/

from __future__ import print_function
# from pprint import pprint

########################################################################

DEBUG = False

########################################################################


def distance(n1, n2):
    """Compute the 'distance' between two string representations of equal
    length integers."""

    return sum(                          # sum of True
        [                                # elements in this list
            x != y for                   # Boolean True if different
            (x, y) in zip(               # side-by-side characters
                * map(                   # side-by-side lists
                    list,                # list of characters
                    map(
                        str,             # convert to string
                        [n1, n2]
                    )
                )
            )
        ]
    )

########################################################################


def compute_tree(l):
    """Shortest chain from first item to last item."""
    # results is a dictionary of adjacent nodes: {node : [list of adjacencies]}
    results = {}

    # edges contains adjacent number pairs: [(from, to) ...]
    edges = []

    # compute tree for all nodes except last
    for item in l[:-1]:

        # start with empty list of adjacent places
        nearest_list = []

        # check adjacencies to all other nodes, both directions
        for item2 in l:

            # if nodes are adjacent, record them
            if distance(item, item2) == 1:
                nearest_list.append(item2)
                edges.append((item, item2))

        # keep the branches of nearby nodes
        results[item] = nearest_list

    return results, edges

########################################################################


def backtrack(end, revisited, edges):

    kv = {}
    for k, v in revisited:
        kv.setdefault(k, [])
        kv[k].append(v)

    result = []
    last = sorted(kv)[-1]
    next_node = end
    result.append(next_node)
    for i in range(last - 1, 0, -1):
        nodelist = kv[i]
        for node in nodelist:
            if (node, next_node) in edges:
                next_node = node
                result.append(next_node)
                break
    result.reverse()
    return result

########################################################################


def traverse_tree(l, tree, edges):
    """Traverse the tree in l from l[0] to l[-1]."""

    start = l[0]
    end = l[-1]

    if DEBUG:
        print("start", start)
        print("end", end)

    # create a dictionary of visited nodes
#   visited = dict((x, 0) for x in l)
    from collections import OrderedDict
    visited = OrderedDict()

    # finding first frontier_level of frontier
    frontier_level = 1

    # first frontier_level is automatically visited by being placed on the
    # new_frontier
    visited[start] = frontier_level
    new_frontier = [start]

    # while there is a new_frontier
    while new_frontier:

        # set it as the working frontier
        working_frontier = new_frontier

        # bump the frontier_level
        frontier_level += 1

        # empty the new_frontier
        new_frontier = []

        # search the working frontier
        while working_frontier:

            # one node at a time
            loc = working_frontier.pop()

            # if the end has not been reached
            if loc != end:

                # collect the new frontier
                for next in tree[loc]:

                    # skipping already-visited locations
                    if visited.get(next, 0):
                        continue

                    visited[next] = frontier_level
                    new_frontier.append(next)

                # continue with the next frontier item
                continue

            else:

                # reached the end; get the nodes in 'frontier_level' order
                if DEBUG:
                    print("visited", visited)
                revisited = sorted(
                    [(y, x) for x, y in visited.items() if y != 0]
                )

                # compute the path by backtracking
                return backtrack(end, revisited, edges)

    # never finished?!
    return []

########################################################################


def checkio(l):
    # parse the tree
    tree, edges = compute_tree(l)

    # traverse the tree
    result = traverse_tree(l, tree, edges)

    if DEBUG:
        print()
        print("checkio")
        print("l", l)
        print("tree", sorted(tree))
        print("edges", sorted(edges))
        print("result", result)
        print()

    return result

if __name__ == "__main__":
    assert checkio([123, 991, 323, 321, 329, 121, 921, 125, 999]) == [123, 121, 921, 991, 999]
    assert checkio([111, 222, 333, 444, 555, 666, 121, 727, 127, 777]) == [111, 121, 127, 727, 777]
    assert checkio([456, 455, 454, 356, 656, 654]) == [456, 454, 654]  # or [456, 656, 654]
    assert checkio([275, 867, 459, 224, 962, 132, 405, 430, 271, 724, 161, 740, 225, 484, 414, 814, 976, 869, 914, 241]) == [275, 271, 241]
    print("Done!")

# end of file
