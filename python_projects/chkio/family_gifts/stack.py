# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

# https://py.checkio.org/mission/family-gifts/

########################################################################

from __future__ import print_function

########################################################################

from collections import defaultdict, deque
from pprint import pformat

########################################################################

DEBUG = True

########################################################################


def normalize(path, family0):
    """Rotate the circular path to have 'family0' at the start"""

    d = deque(path)
    if family0 not in d:
        return path

    while d[0] != family0:
        d.rotate(-1)
    return list(d)

########################################################################

# http://stackoverflow.com/questions/13089352/
#   how-can-i-figure-out-who-can-give-gifts-to-whom-on-christmas


def calc_gifts(names, blacklist, gifts={}):
    """Calculate gift circles."""
    if len(names) > 0:
        name, rest = names[0], names[1:]
        for other in names + list(gifts):
            if (other != name and
                    other not in blacklist[name] and
                    (other not in gifts or gifts[other] != name) and
                    other not in gifts.values()):

                gifts_new = dict(gifts.items() + [(name, other)])
                for solution in calc_gifts(rest, blacklist, gifts_new):
                    yield solution
    else:
        yield gifts

########################################################################


def unwrap(dictionary_list, n0):
    """Unwrap the solution list of dictionaries, starting each with n0."""
    out = []
    for solution_dict in dictionary_list:
        result = [n0]
        next = solution_dict[n0]
        while next != n0:
            result.append(next)
            next = solution_dict[next]
        if DEBUG:
            print(result)
        out.append(tuple(result))
    return out

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
    """Find chains of gift-givers in 'family', excuding 'couples'.

    Members of 'family' give gifts to each other each year; pairs of members
    that are 'couples' don't give to each other. Compute the chains of giving
    such that no member gives to the same person in another chain."""

    # form the blacklist, pairs of people who cannot exchange gifts
    blacklist = defaultdict(list)
    for x, y in couples:
        blacklist[x].append(y)
        blacklist[y].append(x)

    # convert set to list
    names = list(family)

    # get the alphabetically first name
    name0 = sorted(names)[0]

    # compute all chains, starting them with name0
    solution = unwrap(
        list(
            calc_gifts(names, blacklist)),
        name0
    )

    # keep chains of family length
    solution = set([x for x in solution if len(x) == len(family)])

    if DEBUG:
        print("solution", pformat(solution))

    # keep only the chains having different pairings from one another
    chains = []

    # form a list of solution strings
    p = list([" ".join(list(x)) for x in solution])
    while p:
        # get the topmost solution
        r0 = (p.pop(0)).split()
        if DEBUG:
            print("\nr0", r0)

        # add this solution to the output
        chains.append(
            normalize(
                r0,
                name0
            )
        )

        # form gift-giving pairs
        c0 = r0 + [r0[0]]
        pairs = [" ".join(c0[i:i + 2]) for i in range(len(c0) - 1)]
        if DEBUG:
            print("\npairs", pformat(pairs))
        remove_pairs(pairs, p)

    if DEBUG:
        print("chains", "\n", len(chains), "\n", pformat(chains, width=132))

    return chains

########################################################################
assert len(
    find_chains(
        {"Allison", "Robin", "Petra", "Curtis", "Bobbie", "Kelly"},
        (
            {"Allison", "Curtis"},
            {"Robin", "Kelly"},
        )
    )
) == 4

if 0:
    family = {'Philip', 'Sondra', 'Mary', 'Selena', 'Eric', 'Phyllis'}
    couples = (
        {'Philip', 'Sondra'},
        {'Eric', 'Mary'},
    )

    find_chains(family, couples)

else:

    family = {
        'Loraine', 'Leah', 'Jenifer', 'Russell', 'Benjamin', 'Todd',
        'Maryanne', 'Penny', 'Matthew'
    }

    couples = (
        {"Loraine", "Benjamin"},
        {"Leah", "Matthew"},
        {"Todd", "Jenifer"},
    )

    print(pformat(find_chains(family, couples), width=132))

# end of file
