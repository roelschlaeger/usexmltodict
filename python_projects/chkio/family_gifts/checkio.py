# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

# findAllPaths:
#   http://algohangout.blogspot.com/2015/01/ \
#     graphtheory-using-python.html?view=sidebar

from __future__ import print_function

########################################################################

from collections import defaultdict, deque
from itertools import combinations
from pprint import pformat

########################################################################

DEBUG = False

########################################################################


def prune_circular_duplicates(input_paths):
    """Remove paths that are duplicates after circularly shifting."""
    output_paths = set()
    for path in input_paths:
        d = deque(path)
        m = min([x for x in d])
        while m != d[0]:
            d.rotate(-1)
        output_paths.add(tuple(d))
    return list(output_paths)

########################################################################


def findAllPaths(g, start, end, path=[]):
    if path == []:
        if DEBUG:
            print(
                "\n\n  findAllPaths",
                "\n    g", pformat(g),
                "\n    start", pformat(start),
                "\n    end", pformat(end),
                "\n    path", pformat(path)
            )

    path = path + [start]

    if start == end:
        return [path]

    if start not in g:
        return []

    paths = []

    for node in g[start]:

        if node not in path:
            newpaths = findAllPaths(g, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths

########################################################################


def chain_count(members, combos):

    # edges go both ways for all combinations
    edges = combos + [(y, x) for (x, y) in combos]

    # create a neighbors graph
    g = defaultdict(list)
    for x, y in edges:
        g[x].append(y)

    if DEBUG:
        print(
            "\nchain_count",
            "\n  edges", edges,
            "\n  members", pformat(members),
            "\n  g", pformat(g),
        )

    # success is if all members are included in the chain
    full_length = len(members)

    # create list of original members for (start, end) combinations
    member_pairs = combinations(members, 2)

    # create a list of full_length paths
    full_length_paths = []

    # find all paths for each (start, end) combination
    for start, end in member_pairs:

        # start with an empty pathlist
        path = []

        # collect all paths from start to end, no matter how long
        paths = findAllPaths(g, start, end, path)

        # keep only the paths that include all members and are circular
        full_paths = [
            x for x in paths
            if len(x) == full_length and
            (x[0], x[-1]) in edges
        ]

        if DEBUG:
            print(
                "\n",
                "\n  start", start,
                "\n  end", end,
                "\n  paths", paths,
                "\n  full_paths", full_paths
            )

        # don't keep duplicates, if any
        for full_path in full_paths:
            if full_path not in full_length_paths:
                full_length_paths.append(full_path)

    # now resolve any paths that are the same under circular rotation
    pruned_paths = prune_circular_duplicates(full_length_paths)

    if DEBUG:
        print(
            "\n\n",
            "\n  full_length_paths\n", pformat(full_length_paths),
            "\n  pruned_paths\n", pformat(pruned_paths),
        )

    return pruned_paths

########################################################################


def find_chains(members, groups={}):
    # display the input
    if DEBUG:
        print("\nmembers", members, "groups", pformat(groups))

    # form all the combinations
    c = list(combinations(sorted(members), 2))

    # remove the couples from the combinations
    for group in groups:
        c.remove(tuple(sorted(group)))

    # show the remaining combinations
    if DEBUG:
        print("find_chains",
              "\n  members", pformat(members),
              "\n  groups", pformat(groups),
              "\n  c", pformat(c)
              )

    pruned_paths = chain_count(members, c)

    return pruned_paths

########################################################################

print(
    pformat(
#       find_chains({"Doreen", "Fred", "Yolanda"},  ({"Doreen", "Fred"}, ))
#   )
        find_chains(
            {'Curtis', 'Lee', 'Rachel', 'Javier'},
            (
                {'Rachel', 'Javier'},
                {'Curtis', 'Lee'},
            )
        )
    )
)

# if 1:
#
#     if 1:
#
#         assert find_chains(
#             {'Gary', 'Jeanette', 'Hollie'},
#             (
#                 {'Gary', 'Jeanette'},
#             )
#         ) == 0  # 0 chains
#
#     assert find_chains(
#         {'Curtis', 'Lee', 'Rachel', 'Javier'},
#         (
#             {'Rachel', 'Javier'},
#             {'Curtis', 'Lee'},
#         )
#     ) == 2  # 2 chains
#
# else:
#
#     assert find_chains(
#         {'Beth', 'Curtis', 'Lee', 'Rachel', 'Javier'},
#         (
#             {'Rachel', 'Javier'},
#             {'Curtis', 'Lee'},
#         )
#     ) == 8  # 8 chains

print("Done!")

# end of file
