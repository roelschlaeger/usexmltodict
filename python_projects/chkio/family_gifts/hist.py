# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from itertools import permutations
from pprint import pformat
from collections import deque, defaultdict

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
    try:
        index = [x[0] for x in path].index(family0)
        d = deque(path)
        d.rotate(-index)
        result = list(d)
    except ValueError:
        result = path

    if DEBUG:
        print(
            "\nnormalize"
            "\n  path", pformat(path, width=132),
            "\n  family0", family0,
            "\n  result", result
        )

    return result

########################################################################


def tuple_of_pairs(p):
    """Convert augmented path tuple into tuple of edge tuples."""
    out = []
    for t in p:
        out.append(tuple([tuple(t[i: i + 2]) for i in range(len(t) - 1)]))
    return out

########################################################################


def proto_find_chains(family, couples):
    """Find chains of gift-givers in 'family', excuding 'couples'."""
    """Members of 'family' give gifts to each other each year; pairs of members
    that are 'couples' don't give to each other. Compute the chains of giving
    such that no member gives to the same person in another chain."""

    if DEBUG:
        print(
            "\nproto_find_chains",
            "\n  family", pformat(family),
            "\n  type(family)", type(family),
            "\n  type(family[0])", type(family[0]),
            "\n",
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
        chains.append(normalize(r0, minfam))
        remove_pairs(r0, p)

    if DEBUG:
        print("\n\nsorted(chains)", len(chains), "\n", pformat(sorted(chains)))

    return chains

########################################################################


def verify_chains(list_of_chains):
    """Verify that the chains in the list 'list_of_chains' are valid."""
    if DEBUG:
        print(
            "\nverify_chains",
        )

    for chain in list_of_chains:

        # ensure that all tuples point to their successors
        matches = [
            chain[i][1] == chain[i + 1][0]
            for i in range(-1, len(chain) - 1)
        ]

        fail = not all(matches)

        if DEBUG or fail:
            print(
                "\n  chain", chain,
                "\n  matches", matches,
                "\n  fail", fail
            )

########################################################################


def print_chain(index, chain):
    """Display the 'index'th chain."""
    froms = [x[0] for x in chain]
    print("  %2d" % (index + 1), ", ".join(froms))

########################################################################


def print_chains(chains):
    """Print all chain in 'chains'."""
    for index, chain in enumerate(chains):
        print_chain(index, chain)

########################################################################


def print_possible_chains(possible_chains):
    """Display the contents of 'possible_chains'."""
    for length, chains in possible_chains.items():
        print(
            "\n=================",
            "\n= # chains =", length, " =",
            "\n================="
        )

        for index, chain in enumerate(chains):
            print("Solution group: %d" % (index + 1))
            print_chains(chain)
            print()

########################################################################


def ensure_correct_types(family, couples):
    """Coerce correct data structure types for 'family' and 'couples'."""
    if type(family) == set:
        family = list(family)

    assert type(family) in (list, tuple), \
        "family is of type %s" % type(family)
    assert type(family[0]) == str, \
        "family[0] is of type %s" % type(family[0])

    assert type(couples) in (list, tuple), \
        "couples is of type %s" % type(couples)
    assert type(couples[0]) == set, \
        "couples[0] is of type %s" % type(couples[0])

    family = sorted(list(family))
    couples = sorted(list(couples))
    # convert couples to be tuples instead of sets
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

    return family, couples

########################################################################


def compute_max_length(family, couples):
    """The maximum number of chains is the minumum of edges from all nodes."""
    result = defaultdict(list)

    # add edges between all family members
    [result[x].extend(sorted(list(set(family) - set([x])))) for x in family]
    result = dict(result)

    if DEBUG:
        print(pformat(result, width=132))

    # remove edges between couples
    for a, b in couples:
        result[a].remove(b)
        result[b].remove(a)

    if DEBUG:
        print(pformat(result, width=132))

    minval = min([len(x) for x in result.values()])

    if DEBUG:
        print("compute_max_length", minval)

    return minval

########################################################################


def find_chains(family, couples):
    """Compute chains from all possible starting family members."""
    # coerce to get the correct data structure types
    family, couples = ensure_correct_types(family, couples)

    max_expected_length = compute_max_length(family, couples)

    family_deque = deque(family)
    if DEBUG:
        print(
            "\nfind_chains",
            "\n  family_deque", pformat(family_deque),
            "\n  couples", pformat(couples),
            "\n################################################"
        )

    # compute all chain groups with different ordering of family
    possible_chains = defaultdict(list)
    for i in range(len(family)):

        if DEBUG:
            print(
                "\ni =", i,
                "\n  family_deque", family_deque,
                "\n  couples", couples,
                "\n"
            )

        list_of_chains = proto_find_chains(list(family_deque), couples)

        if DEBUG:
            print(
                "\n\nlist_of_chains", len(list_of_chains),
                "\n", pformat(sorted(list_of_chains), width=132)
            )

        # optional verify of pairs in the result
        verify_chains(list_of_chains)

        # add this solution to the list
        possible_chains[len(list_of_chains)].append(list_of_chains)

        if len(list_of_chains) >= max_expected_length:
            break

        # try the next rotation of the family
        family_deque.rotate(-1)

    # convert to ordinary dict
    possible_chains = dict(possible_chains)

    # find the longest list(s)
    max_key = max(possible_chains.keys())

    if DEBUG:
        print_possible_chains(possible_chains)

    # return one of the lists
    result_chain = possible_chains[max_key][0]
    if 1 or DEBUG:
        print("result_chain", pformat(result_chain))

    if result_chain:
        result = [[x[0] for x in y] for y in result_chain]
    else:
        result = []

    if 1 or DEBUG:
        print(
            "\nfind_chains",
            "\n  result", pformat(result)
        )

    return result

########################################################################

if __name__ == '__main__':

    # find_chains({"Doreen", "Fred", "Yolanda"},  ({"Doreen", "Fred"}, ))

    # find_chains(
    #     {"Nelson", "Kaitlin", "Amelia", "Jack"},
    #     (
    #         {"Kaitlin", "Jack"},
    #         {"Nelson", "Amelia"},
    #     )
    # )

    family = {
        'Loraine', 'Leah', 'Jenifer', 'Russell', 'Benjamin', 'Todd',
        'Maryanne', 'Penny', 'Matthew'
    }

    couples = (
        {"Loraine", "Benjamin"},
        {"Leah", "Matthew"},
        {"Todd", "Jenifer"},
    )
    #
    # family = {'Philip', 'Sondra', 'Mary', 'Selena', 'Eric', 'Phyllis'}
    # couples = ({'Philip', 'Sondra'}, {'Eric', 'Mary'},)

    # family = {"Allison",  "Robin",  "Petra",  "Curtis",  "Bobbie",  "Kelly"}
    # couples = ({"Allison",  "Curtis"},  {"Robin",  "Kelly"},)

    result = find_chains(family, couples)
    print("\nresult", len(result), pformat(result, width=132, depth=3))

# end of file
