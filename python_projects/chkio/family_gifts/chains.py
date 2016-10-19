# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from collections import defaultdict
from pprint import pformat

########################################################################

EDGES = [
    ('Beth', 'Curtis'), ('Beth', 'Javier'), ('Beth', 'Lee'), ('Beth', 'Rachel'),
    ('Curtis', 'Javier'), ('Curtis', 'Rachel'),
    ('Javier', 'Curtis'), ('Javier', 'Lee'),
    ('Lee', 'Javier'), ('Lee', 'Rachel'),
    ('Rachel', 'Curtis'), ('Rachel', 'Lee')
]

########################################################################


def recurse(depth, pairs, p0, m0, l0):

    m1 = m0.copy()
    m1.remove(p0)
#   l0.append(p0)

#   print("m1", m1)
#   if m1 == set([]):
#       print(" " * depth, l0 + [p0])

    for p1 in pairs[p0]:
        if p1 in m1:
#           print(" " * depth, p1)
            recurse(depth + 1, pairs, p1, m1, l0 + [p0])

    print("l0", l0)
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
    result = recurse(0, pairs, p0, m0, l0)
    print(result)
    return result

########################################################################


def build_chains(edges):
    m = set([x[0] for x in edges])

    pairs = defaultdict(list)
    for f, t in edges:
        pairs[f].append(t)

    print("build_chains",
          "\nm", pformat(m),
          "\nedges", pformat(edges),
          "\npairs", pformat(pairs),
          )

    print()
    m0 = m.copy()
    p0 = list(m0)[0]

    print("p0", p0)

    results = []
    m1 = m0.copy()
    m1.remove(p0)
    for p1 in pairs[p0]:
        if p1 in m1:
            print(" p1", p1)

            m2 = m1.copy()
            m2.remove(p1)
            for p2 in pairs[p1]:
                if p2 in m2:
                    print("  p2", p2)

                    m3 = m2.copy()
                    m3.remove(p2)
                    for p3 in pairs[p2]:
                        if p3 in m3:
                            print("   p3", p3)
                            m3.remove(p3)
                            results.append((p0, p1, p2, p3))

    print()
    print(pformat(results))
    print()

########################################################################

if __name__ == "__main__":

#   build_chains(EDGES)
    alt_chains(EDGES)

# end of file
