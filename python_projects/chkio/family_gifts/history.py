# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

from __future__ import print_function

# https://py.checkio.org/mission/family-gifts/

# findAllPaths:
#   http://algohangout.blogspot.com/2015/01/ \
#     graphtheory-using-python.html?view=sidebar

########################################################################

DEBUG = False

########################################################################

from collections import defaultdict
from itertools import combinations
from pprint import pformat

########################################################################


def findAllPaths(g, start, end, path=[]):
    """Find all paths in 'g' between 'start' and 'end'."""

    # show parameters on the first recursion
    if path == []:
        if DEBUG:
            print(
                "\n\n  findAllPaths",
                "\n    g", pformat(g),
                "\n    start", pformat(start),
                "\n    end", pformat(end),
                "\n    path", pformat(path)
            )

    # extend the
    path = path + [start]

    # check for completion
    if start == end:
        return [path]

    if start not in g:
        return []

    # build a list of paths
    paths = []

    # check the next node in the graph
    for node in g[start]:

        # if not visited yet
        if node not in path:

            # recurse
            newpaths = findAllPaths(g, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths

########################################################################


def normalize(path, family0):
    """Rotate the circular path to have 'family0' at the start"""

    from collections import deque
    d = deque(path)
    while d[0] != family0:
        d.rotate(-1)
    return list(d)

########################################################################


def find_chains(family, couples):

    # put the family in sorted order so that combinations will be in order, too
    family = sorted(list(family))

    # put couples in order so they can be found in l2 combinations
    couples = [tuple(sorted([x, y])) for (x, y) in couples]

    # form all combinations of two family members
    l2 = list(combinations(family, 2))

    # remove couples from combinations
    for couple in couples:
        l2.remove(couple)

    # form permutations from combinations
    p2 = l2 + [(y, x) for (x, y) in l2]

    # compute edge graph dictionary from permutations
    edges = defaultdict(list)
    [edges[x].append(y) for (x, y) in p2]

    # make into ordinary dictionary
    edges = dict(edges)

    if DEBUG:
        print("family", family)
        print("couples", couples)
        print("l2", pformat(l2))
        print("edges", pformat(edges))

    # compute all full-length paths between all (start, end) pairs
    paths = defaultdict(list)
    for start, end in l2:
        if start in edges[end]:
            paths[(start, end)] = [
                x for x in findAllPaths(
                    edges, start, end
                ) if len(x) == len(family)
            ]

    # accumulate all paths starting from family[0]
    apaths = []
    [apaths.extend(paths[x]) for x in paths]
    if DEBUG:
        print("apaths", pformat(apaths))

    # append reversed paths
    reversed_paths = [list(reversed(x)) for x in apaths]
    if DEBUG:
        print("reversed_paths", reversed_paths)

    apaths += reversed_paths
    if DEBUG:
        print("apaths", pformat(apaths))

    # convert to space-separated strings for easier searching
    spaths = [" ".join(x) for x in apaths]
    if DEBUG:
        print("spaths", pformat(spaths))

    remaining, last_firsts = [], set()
    while spaths:

        # get a remaining path
        r0 = spaths.pop(0).split()
        if DEBUG:
            print("r0", r0)

        # check for last->first duplicates
        last_first = (r0[-1], r0[0])
        if DEBUG:
            print("last_first", last_first)

        if last_first not in last_firsts:
            remaining.append(normalize(r0, family[0]))
            last_firsts.add(last_first)

        # split path into pairs
        ap = [" ".join(r0[i:i + 2]) for i in range(len(r0) - 1)]
        ap.append(" ".join([r0[-1], r0[0]]))
        if DEBUG:
            print("ap", ap)

        # find all remaining paths having the pairs
        rkeys = []
        for akey in ap:
            rkeys.extend([x for x in spaths if x.find(akey) != -1])
        rkeys = list(set(rkeys))

        if DEBUG:
            print("rkeys", pformat(rkeys))

        # remove the paths from further consideration
        [spaths.remove(x) for x in rkeys]
        if DEBUG:
            print("spaths", len(spaths), pformat(spaths))

    # all that is left is in 'remaining'
    if DEBUG:
        print("remaining", pformat(remaining))

    result = remaining

    return result

########################################################################

family = {'Allison', 'Robin', 'Petra', 'Curtis', 'Bobbie', 'Kelly'}
couples = [('Allison', 'Curtis'), ('Kelly', 'Robin')]
# family = {'A', 'R', 'P', 'C', 'B', 'K'}
# couples = [('A', 'C'), ('K', 'R')]
remaining = find_chains(family, couples)
print("\nfind_chains(\n",
      pformat(family),
      ", \n",
      pformat(couples),
      ") = \n",
      pformat(remaining)
      )

########################################################################
