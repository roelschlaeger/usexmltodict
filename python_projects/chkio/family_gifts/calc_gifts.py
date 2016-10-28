# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

########################################################################

from __future__ import print_function

########################################################################

from collections import defaultdict
from itertools import permutations

########################################################################


def unwind(solution_dict, n0):
    """Convert path dictionary to a list beginning with 'n0'."""
    result = [n0]
    next = solution_dict[n0]
    while next != n0:
        result.append(next)
        next = solution_dict[next]
#   if DEBUG:
#       print(result)
    return result

########################################################################


def create_blacklist(couples, edges=None):
    """Create the blacklist from the couples pairs."""
    # form the blacklist, pairs of people who cannot exchange gifts
    blacklist = defaultdict(list)
    for x, y in couples:
        blacklist[x].append(y)
        blacklist[y].append(x)

    if edges is not None:
        for from_edge, to_edge in edges:
            blacklist[from_edge].append[to_edge]

    return blacklist

########################################################################

# http://stackoverflow.com/questions/13089352/
#   how-can-i-figure-out-who-can-give-gifts-to-whom-on-christmas


def calc_gifts(names, blacklist, gifts={}):
    """Calculate gift circles."""
    # any names left to process?
    if len(names) > 0:

        # split off one name from the rest
        name, rest = names[0], names[1:]

        # look at all names and gift donors for extending the chain
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


def compute_graphs(family, blacklist):
    """Compute from and to graphs from 'family' and 'blacklist'."""
    g_from = defaultdict(list)
    g_to = defaultdict(list)
    for p_from, p_to in permutations(family, 2):
        # print((p_from, p_to))
        if p_to not in blacklist[p_from]:
            g_from[p_from].append(p_to)
            g_to[p_to].append(p_from)
    return g_from, g_to

########################################################################

if __name__ == "__main__":

    from pprint import pformat, pprint

    DEBUG = True

    family = {
        'Loraine', 'Leah', 'Jenifer', 'Russell', 'Benjamin', 'Todd',
        'Maryanne', 'Penny', 'Matthew'
    }

    couples = (
        {"Loraine", "Benjamin"},
        {"Leah", "Matthew"},
        {"Todd", "Jenifer"},
    )

    ####################################################################

    def print_dict(dname, d):
        print(dname)
        print('=' * len(dname))
        print()
        for k in sorted(d):
            print(
                "\n", k,
                "\n", len(d[k]), pformat(d[k], width=132)
            )
        print()

    ####################################################################

    def calc_via_triples(triples, family, couples):
        print("\n\n\ncalc_via_triples")
        print("\n  len(triples)", len(triples))
        for triple in triples[:3]:
            print("\n  triple", pformat(triple))
            pre, mid, post = triple
            fam2 = family - set([mid, post])
            print("\n  fam2", fam2)
            blacklist2 = create_blacklist(couples)
            shorter_paths = list(calc_gifts([post] + list(fam2), blacklist2))
            short = [
                y for y in [unwind(x, post) for x in shorter_paths]
                if len(y) >= len(fam2) and y[-1] == pre
            ]
            print(
                "\n  len(shorter_paths)", len(shorter_paths),
                "\n  shorter_paths[:2]", pformat(shorter_paths[:2]),
                "\n...",
                "\n  len(short)", len(short),
                "\n  short[:2]", pformat(short[:2]),
                "\n..."
            )

    ####################################################################

    def find_chain(family, couples, paths=[]):
        """Find a chain of gift-givers in 'family', excluding 'couples'."""
        """Members of 'family' give gifts to each other each year; pairs of
        members that are 'couples' don't give to each other. Compute the chains
        of giving such that no member gives to the same person in another
        chain."""

        if DEBUG:
            print(
                "\nfind_chain",
                "\n  family", pformat(family),
                "\n  couples", pformat(couples),
                "\n  paths", pformat(couples)
            )
        # create the initial blacklist from couples
        blacklist = create_blacklist(couples)

        # add to the blacklist to reflect previous paths
        for path in paths:
            for k, v in path.items():
                if v not in blacklist[k]:
                    blacklist[k].append(v)

        if DEBUG:
            print("\n  blacklist", pformat(dict(blacklist)))

        g_from, g_to = compute_graphs(family, blacklist)
        if DEBUG:
            print_dict("g_from", g_from)
            print_dict("g_to", g_to)

        ################################################################

        # take one of the couples
        choice = list(couples[0])[0]
        to_choices = g_to[choice]
        from_choices = g_from[choice]

        triples = [
            [
                (x, choice, z) for x in to_choices if x != z
            ] for z in from_choices
        ]

        pprint(triples, width=132)

        for triple0 in triples:
            calc_via_triples(triple0, family, couples)

        # return calc_gifts(list(family), blacklist)
        return "No result generated"

    result = list(find_chain(family, couples))
    print("len(result)", len(result))

# end of file
