# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from collections import defaultdict
from pprint import pformat

########################################################################


def recurse(depth, pairs, p0, m0, l0, result):

    m1 = m0.copy()
    m1.remove(p0)

    if m1 == set([]):
        result.append(l0 + [p0])

    for p1 in pairs[p0]:
        if p1 in m1:
            recurse(depth + 1, pairs, p1, m1, l0 + [p0], result)

    return l0

########################################################################


def alt_chains(edges):
    m = set([x[0] for x in edges])

    pairs = defaultdict(list)
    for f, t in edges:
        pairs[f].append(t)

    m0 = m.copy()
    p0 = list(m0)[0]
    l0 = []
    result = []

    recurse(0, pairs, p0, m0, l0, result)

    return result

########################################################################

if __name__ == "__main__":

    EDGES = [
#       ('Alex', 'Beth'),
#       ('Alex', 'Lee'),

#       ('Beth', 'Curtis'),
#       ('Beth', 'Javier'),
        ('Beth', 'Lee'), ('Beth', 'Rachel'),

        ('Curtis', 'Javier'), ('Curtis', 'Rachel'),

        ('Javier', 'Curtis'), ('Javier', 'Lee'),

        ('Lee', 'Javier'), ('Lee', 'Rachel'),

        ('Rachel', 'Curtis'), ('Rachel', 'Lee')
    ]

    result = alt_chains(EDGES)
    print(pformat(result))

# end of file
