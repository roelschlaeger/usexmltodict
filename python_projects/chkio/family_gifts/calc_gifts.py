# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

########################################################################

from __future__ import print_function

########################################################################

from collections import defaultdict
from itertools import permutations

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

        # convert set to list
        names = list(family)

        ################################################################

        # take one of the couples
        choice = couples[0][0]
        to_choices = g_to[choice]
        from_choices = g_from[choice]

        triples = [
            [
                (x, choice, z) for x in to_choices if x != z
            ] for z in from_choices
        ]

        pprint(triples)

        return calc_gifts(names, blacklist)

    result = list(find_chain(family, couples))
    print("len(result)", len(result))

# end of file
