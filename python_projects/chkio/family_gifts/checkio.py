# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

# from collections import Counter
from ap import findAllPaths
from collections import defaultdict
from itertools import combinations
from pprint import pformat


########################################################################

DEBUG = True

########################################################################


def chain_count(members, c):

    # graph to contain edges going both ways
    bidir = c + [(y, x) for (x, y) in c]
    print("\ng", bidir)

    g = defaultdict(list)
    for x, y in bidir:
        g[x].append(y)

    print(
        "\nchain_count",
        "\n  members", pformat(members),
        "\n  g", pformat(g)
    )

    full_length = len(members)
    member_pairs = combinations(members, 2)
    full_length_paths = []

    for start, end in member_pairs:
        path = []
        paths = findAllPaths(g, start, end, path)
        full_paths = [x for x in paths if len(x) == full_length]

        print(
            "\nchain_count",
            "\n  start", start,
            "\n  end", end,
            "\n  paths", paths,
            "\n  full_paths", full_paths
        )

        for full_path in full_paths:
            if full_path not in full_length_paths:
                full_length_paths.append(full_path)

    result = len(full_length_paths)
    print(
        "\n\nchain_count",
        "\n  full_length_paths\n", pformat(full_length_paths),
        "\n  result", result
    )
    return result

########################################################################


def find_chains(members, groups={}):
    # display the input
    print("\nmembers", members, "groups", pformat(groups))

    # form all the combinations
    c = list(combinations(sorted(members), 2))

    # remove the couples from the combinations
    for group in groups:
        c.remove(tuple(sorted(group)))

    # show the remaining combinations
    print("find_chains",
          "\n  members", pformat(members),
          "\n  groups", pformat(groups),
          "\n  c", c
          )

    n = chain_count(members, c)

    return n

########################################################################

if 1:

    if 0:

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
