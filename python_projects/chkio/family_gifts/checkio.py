# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from collections import Counter
from itertools import combinations
from pprint import pformat
from collections import defaultdict

########################################################################

DEBUG = True

########################################################################


def print_chains(c):
    edges = sorted(c + [(y, x) for (x, y) in c])
    c_edges = Counter([x[0] for x in edges])
    min_c_edges = min(c_edges.values())
    m = set([x[0] for x in edges])

    pairs = defaultdict(list)
    for f, t in edges:
        pairs[f].append(t)
    print("print_chains",
          "\n    edges", pformat(edges),
          "\n    c_edges", pformat(c_edges),
          "\n    min_c_edges", min_c_edges,
          "\n    m", pformat(m),
          "\n    pairs", pformat(pairs)
          )

    chains = []
#   stack = [edges[0]]

    print("chains", pformat(chains))

########################################################################


def find_chains(members, groups={}):
    # display the input
    print("\nmembers", members, "groups", pformat(groups))

    # verify the input
    for group in groups:
        for name in group:
            assert name in members, "%s is missing from members" % name

    result = 0

    # form all the combinations
    c = list(combinations(sorted(members), 2))

    # remove the couples from the combinations
    for group in groups:
        c.remove(tuple(sorted(group)))

    # show the remaining combinations
    print(pformat(c))

    if len(c) >= len(members):

        givers = [x[0] for x in c]
        print("givers", givers)

        counts = Counter(givers)
        print("counts", pformat(counts))

        result = max(counts.values())

    if DEBUG:
        print_chains(c)

    print("result", result)
    return result

########################################################################

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
