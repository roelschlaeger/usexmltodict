# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from itertools import permutations
from pprint import pformat
from collections import deque

########################################################################

DEBUG = False

########################################################################


def remove_pairs(pairs, p):
    """Remove elements from p that contain elements in pairs."""
    if DEBUG:
        print(
            "\nremove_pairs",
            "\n  type(pairs)", type(pairs),
            "\n  type(pairs[0])", type(pairs[0]),
            "\n  type(p)", type(p),
            "\n  pairs", pformat(pairs, width=132)
        )

    removables = []
    for pair in pairs:
        removables.extend([tuple(x) for x in p if pair in x])
    removables = set(removables)

    if DEBUG:
        print(
            "\n====",
            "\n", len(p),
            "-",
            len(removables),
            "=",
            len(p) - len(removables),
            "\nremovables", pformat(list(removables)[:3], width=132)
        )

    for match in removables:
        p.remove(match)

    if DEBUG:
        print(
            "\np", len(p),
            "\n", pformat(p[:3], width=132)
        )

########################################################################


def normalize(path, family0):
    """Rotate the circular path to have 'family0' at the start."""
    return path  # FIXME

    d = deque(path)
    index = d.index(family0)
    d.rotate(-index)
#   while d[0] != family0:
#       d.rotate(-1)
    return list(d)

########################################################################


def tuple_of_pairs(p):
    """Convert augmented path tuple into tuple of edge tuples."""
    out = []
    for t in p:
        out.append(tuple([tuple(t[i: i + 2]) for i in range(len(t) - 1)]))
    return out

########################################################################


def find_chains(family, couples):
    """Find chains of gift-givers in 'family', excuding 'couples'."""
    """Members of 'family' give gifts to each other each year; pairs of members
    that are 'couples' don't give to each other. Compute the chains of giving
    such that no member gives to the same person in another chain."""

    if DEBUG:
        print(
            "\nfind_chains",
            "\n  family", pformat(family),
            "\n  type(family)", type(family),
            "\n  type(family[0])", type(family[0]),
            "\n",
            "\n  couples", pformat(couples),
            "\n  type(couples)", type(couples),
            "\n  type(couples[0])", type(couples[0]),
            "\n"
        )

    assert type(family) in (list, tuple), \
        "family is of type %s" % type(family)
    assert type(family[0]) == str, \
        "family[0] is of type %s" % type(family[0])

    assert type(couples) in (list, tuple), \
        "couples is of type %s" % type(couples)
    assert type(couples[0]) in (set,), \
        "couples[0] is of type %s" % type(couples[0])

    family = list(family)
    couples = sorted(list(couples))
    if type(couples[0]) == set:
        couples = [tuple(sorted([x, y])) for (x, y) in couples]
        if DEBUG:
            print(
                "\n  *** retyped couples ***",
                "\n  couples", pformat(couples),
                "\n  type(couples)", type(couples),
                "\n  type(couples[0])", type(couples[0]),
                "\n"
            )

    minfam = sorted(family)[0]

    # get the first family member
    f0 = family.pop(0)
    if DEBUG:
        print("  f0", f0)

    # compute permutations wrapped by first member
    p = tuple_of_pairs([
        ((f0,) + x + (f0,))
        for x in permutations(
            family, len(family)
        )
    ])

    if DEBUG:
        print(
            "\n  p", len(list(p)), pformat(p[:3], width=132)
        )

    # couples cannot gift each other
    couple_pairs = [(x, y) for (x, y) in couples] + \
        [(y, x) for (x, y) in couples]

    if DEBUG:
        print(
            "\n  couple_pairs", couple_pairs)

    remove_pairs(couple_pairs, p)

    chains = []
    while p:
        r0 = p.pop(0)
        if DEBUG:
            print("\nr0", r0)
        chains.append(normalize(r0[:-1], minfam))
#       pairs = [tuple(r0[i:i + 2]) for i in range(len(r0) - 1)]
        remove_pairs(r0, p)

    if DEBUG:
        print("\n\nchains", len(chains), "\n", pformat(chains))

    return chains

########################################################################

# family = {'A', 'R', 'P', 'C', 'B', 'K'}
# couples = [('A', 'C'), ('K', 'R')]

# family = {'Allison', 'Robin', 'Petra', 'Curtis', 'Bobbie', 'Kelly'}
# couples = ({'Allison', 'Curtis'}, {'Kelly', 'Robin'},)

# family = {'Loraine', 'Leah', 'Jenifer', 'Russell', 'Benjamin', 'Todd',
#           'Maryanne', 'Penny', 'Matthew'}
#
# couples = (
#     {"Loraine", "Benjamin"},
#     {"Leah", "Matthew"},
#     {"Todd", "Jenifer"},
# )
#
# print(pformat(find_chains(family, couples)))

# from collections import deque


def chains(family, couples):
    """Compute chains from all possible starting family members."""
    print("chains")
    family = sorted(list(family))
    couples = sorted(list(couples))

    d = deque(family)
    print(
        "\nchains",
        "\n  d", pformat(d),
        "\n  couples", pformat(couples),
        "\n################################################"
    )

    for i in range(len(family)):

        if DEBUG:
            print(
                "\ni =", i,
                "\n  d", d,
                "\n  couples", couples,
                "\n"
            )

        result = find_chains(list(d), couples)

        print(
            "\n\nresult", len(result),
            "\n", pformat(sorted(result), width=132)
        )

        d.rotate(-1)

family = {"Allison",  "Robin",  "Petra",  "Curtis",  "Bobbie",  "Kelly"}
couples = ({"Allison",  "Curtis"},  {"Robin",  "Kelly"},)
chains(family, couples)

# family = {'Philip', 'Sondra', 'Mary', 'Selena', 'Eric', 'Phyllis'}
# couples = (
#     {'Philip', 'Sondra'},
#     {'Eric', 'Mary'},
# )
# chains(family, couples)

# print(pformat(find_chains(
#     {'Philip', 'Sondra', 'Mary', 'Selena', 'Eric', 'Phyllis'},
#     (
#         {'Philip', 'Sondra'},
#         {'Eric', 'Mary'}
#     )
# )))


# end of file
