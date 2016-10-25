# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from itertools import permutations
from pprint import pformat

########################################################################

DEBUG = True

########################################################################


def remove_pairs(pairs, p):
    """Remove elements from p that contain elements in pairs."""
    removables = []
    for pair in pairs:
        removables.extend([x for x in p if x.find(pair) != -1])
    removables = set(removables)

    if DEBUG:
        print(
            "remove_pairs",
            pformat(pairs),
            len(p),
            "-",
            len(removables),
            "=",
            len(p) - len(removables)
        )

    for match in removables:
        p.remove(match)

########################################################################


def find_chains(family, couples):
    """Find chains of gift-givers in 'family', excuding 'couples'."""
    """Members of 'family' give gifts to each other each year; pairs of members
    that are 'couples' don't give to each other. Compute the chains of giving
    such that no member gives to the same person in another chain."""

    # extend the permutations to include cycle
    p = [
        " ".join(x + (x[0],))
        for x in permutations(
            sorted(family), len(family)
        )
    ]
    if DEBUG:
        print("p", len(list(p)), "\n", pformat(list(p)))

    # couples cannot gift each other
    couple_pairs = [
        " ".join(x) for x in couples + tuple((y, x) for (x, y) in couples)
    ]
    if DEBUG:
        print("couple_pairs", couple_pairs)

    remove_pairs(couple_pairs, p)

    chains = []
    while p:
        r0 = (p.pop(0)).split()
        if DEBUG:
            print("\nr0", r0)
        chains.append(r0[:-1])
        pairs = [" ".join(r0[i:i + 2]) for i in range(len(r0) - 1)]
        if DEBUG:
            print("\npairs", pformat(pairs))
        remove_pairs(pairs, p)

    if DEBUG:
        print("chains", pformat(chains))

    return chains

########################################################################

# family = {'A', 'R', 'P', 'C', 'B', 'K'}
# couples = [('A', 'C'), ('K', 'R')]

# family = {'Allison', 'Robin', 'Petra', 'Curtis', 'Bobbie', 'Kelly'}
# couples = ({'Allison', 'Curtis'}, {'Kelly', 'Robin'},)

family = {'Loraine', 'Leah', 'Jenifer', 'Russell', 'Benjamin', 'Todd',
          'Maryanne', 'Penny', 'Matthew'}

couples = (
    {"Loraine", "Benjamin"},
    {"Leah", "Matthew"},
    {"Todd", "Jenifer"},
)

print(pformat(find_chains(family, couples)))

# end of file
