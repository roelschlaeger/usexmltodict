# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from itertools import combinations
from pprint import pformat
from recipe_576723_1 import recursive_dfs as dfs

########################################################################


def path_generator(members, edges):

    for member in members:
        path = dfs(graph, start)
        yield path

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

    paths = path_generator(members, edges)
    while 1:
        path = paths.next()
        print("path", pformat(path))

    return 0

########################################################################

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


