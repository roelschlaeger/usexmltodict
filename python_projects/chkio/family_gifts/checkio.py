# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

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

DEBUG = True

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
    """Find all paths in 'g' between 'start' and 'end'."""
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


def unique_edges(pruned_paths):
    """Find gift lists that have unique pairs of participants."""
    unique_edges_paths = []
    if pruned_paths:
        p0 = pruned_paths.pop()
        unique_edges_paths.append(p0)

        edges_seen = set([(p0[i], p0[i + 1]) for i in range(len(p0) - 2)])
        for path in pruned_paths:
            new_edges = set(
                [(path[i], path[i + 1]) for i in range(len(path) - 2)]
            )
            if new_edges.isdisjoint(edges_seen):
                unique_edges_paths.append(path)
                edges_seen.update(new_edges)
    return unique_edges_paths

########################################################################


def chain_count(family, combos):
    """Count chains."""
    # edges go both ways for all combinations
    edges = combos + [(y, x) for (x, y) in combos]

    # create a neighbors graph
    g = defaultdict(list)
    for x, y in edges:
        g[x].append(y)

    if DEBUG:
        print(
            "\nchain_count",
            "\n  edges", pformat(edges),
            "\n  family", pformat(family),
            "\n  g", pformat(g),
        )

    # success is if all family are included in the chain
    full_length = len(family)

    # create list of original family for (start, end) combinations
    member_pairs = combinations(family, 2)

    # create a list of full_length paths
    full_length_paths = []

    # find all paths for each (start, end) combination
    for start, end in member_pairs:

        # start with an empty pathlist
        path = []

        # collect all paths from start to end, no matter how long
        paths = findAllPaths(g, start, end, path)

        # keep only the paths that include all family and are circular
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

    unique_paths = unique_edges(pruned_paths)

    if DEBUG:
        print(
            "\n\n",
            "\n  full_length_paths\n", pformat(full_length_paths),
            "\n  pruned_paths\n", pformat(pruned_paths),
            "\n  unique_paths\n", pformat(unique_paths),
        )

    return unique_paths

########################################################################


def find_chains(family, couples={}):
    """Find chains."""
    # display the input
    if DEBUG:
        print("\nmembers", family, "couples", pformat(couples))

    # form all the combinations
    c = list(combinations(sorted(family), 2))

    # remove the couples from the combinations
    for group in couples:
        c.remove(tuple(sorted(group)))

    # show the remaining combinations
    if DEBUG:
        print("find_chains",
              "\n  family", pformat(family),
              "\n  couples", pformat(couples),
              "\n  c", pformat(c)
              )

    pruned_paths = chain_count(family, c)

    print(
        "\n\n\n**** ", len(pruned_paths),
        "\n", pformat(pruned_paths)
    )

    return len(pruned_paths)

########################################################################


if __name__ == '__main__':
    find_chains(
        {"Allison", "Robin", "Petra", "Curtis", "Bobbie", "Kelly"},
        (
            {"Allison", "Curtis"},
            {"Robin", "Kelly"},
        )
    )

    import sys
    sys.exit(0)

    # These "asserts" using only for self-checking and not necessary for
    # auto-testing
    def checker(function, family, couples, total):
        user_result = function(family.copy(), tuple(c.copy() for c in couples))
        if (not isinstance(user_result, (list, tuple)) or
                any(
                    not isinstance(
                        chain, (list, tuple)
                    ) for chain in user_result
                )):
            return False
        if len(user_result) < total:
            return False
        gifted = set()
        for chain in user_result:
            if set(chain) != family or len(chain) != len(family):
                return False
            for f, s in zip(chain, chain[1:] + [chain[0]]):
                if {f, s} in couples:
                    return False
                if (f, s) in gifted:
                    return False
                gifted.add((f, s))
        return True

    assert checker(
        find_chains,
        {'Gary', 'Jeanette', 'Hollie'},
        (
            {'Gary', 'Jeanette'},
        ),
        0
    ), "Three of us"

    assert checker(
        find_chains,
        {'Curtis', 'Lee', 'Rachel', 'Javier'},
        (
            {'Rachel', 'Javier'},
            {'Curtis', 'Lee'}
        ),
        2
    ), "Pairs"

    assert checker(
        find_chains,
        {'Philip', 'Sondra', 'Mary', 'Selena', 'Eric', 'Phyllis'},
        (
            {'Philip', 'Sondra'},
            {'Eric', 'Mary'}
        ),
        4
    ), "Pairs and Singles"


# print(
#     pformat(
#         find_chains({"Doreen", "Fred", "Yolanda"},  ({"Doreen", "Fred"}, ))
#     )
# )
#
# import sys
# sys.exit(0)
#
# print(
#     pformat(
#         find_chains(
#             {'Curtis', 'Lee', 'Rachel', 'Javier'},
#             (
#                 {'Rachel', 'Javier'},
#                 {'Curtis', 'Lee'},
#             )
#         )
#     )
# )
#
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
