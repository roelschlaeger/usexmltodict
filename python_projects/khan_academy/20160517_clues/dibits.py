# coding=utf-8

"""This module contains the encoding of the cipher message."""

from __future__ import print_function

# The cipher in 9210801046_586c49b847_c.jpg is composed of two two-bit pairs,
# as follows:
#
#     0
#     |
# 3 --.-- 1
#     |
#     2
#
#   2   1
#    \ /
#     .
#    / \
#   3   0
#
# These dibit pairs are encoded by octant2.py into the tuple array shown below:

DIBITS = [
    (2, 0), (3, 1), (2, 2),
    (2, 3), (0, 0), (3, 1),
    (3, 0), (0, 3), (0, 2),
    (2, 0), (2, 2), (0, 2),
    (3, 2), (2, 0), (1, 3),
    (3, 1), (0, 1), (3, 0),
    (0, 1), (3, 2), (0, 1),
    (0, 0), (2, 2), (0, 3),
    (3, 1), (2, 1), (2, 1),
    (1, 0), (0, 1), (2, 2),
    (1, 1), (1, 1), (2, 0),
    (0, 3), (1, 3), (0, 1),
    (2, 2), (2, 0), (2, 0),
    (2, 0), (2, 2), (3, 1),
    (2, 0), (1, 1), (2, 1),
    (1, 1), (3, 1), (2, 2),
    (3, 0), (3, 1), (0, 3),
    (2, 0), (2, 3), (1, 0),
    (1, 2), (1, 3), (0, 0),
    (3, 2), (2, 1), (1, 1),
    (2, 2), (0, 2), (0, 0),
    (1, 0), (3, 3), (0, 2),
    (3, 1), (2, 0), (3, 3),
    (0, 1), (1, 2), (0, 3),
    (1, 3), (3, 1), (3, 2),
    (2, 1), (0, 2), (0, 3),
    (0, 0), (3, 2), (1, 0),
    (1, 0), (1, 3), (0, 3),
    (1, 0), (2, 1), (3, 3),
    (1, 0), (0, 2), (0, 0),
    (3, 0), (2, 1), (3, 3),
    (1, 0), (0, 1), (0, 1),
    (0, 3), (0, 2), (3, 1),
    (0, 2), (2, 1), (2, 3),
    (3, 0), (1, 2), (0, 1),
    (1, 2), (2, 2), (0, 0),
    (0, 1), (1, 1), (3, 3),
    (0, 0), (1, 0), (1, 3),
    (2, 3), (0, 1), (2, 1),
    (0, 2), (2, 0), (1, 1),
    (0, 2), (3, 2), (3, 0),
    (3, 3), (2, 1), (3, 1),
    (2, 0), (0, 2), (1, 2),
    (3, 1), (3, 0), (0, 0),
    (3, 0), (1, 2), (3, 0),
    (1, 1), (0, 1), (0, 3),
    (0, 1), (0, 1), (2, 1),
    (2, 2), (0, 2), (3, 0),
    (2, 0), (0, 1), (2, 2),
    (2, 1), (3, 2), (2, 1),
    (0, 2), (0, 2), (3, 3),
    (2, 0), (2, 1), (1, 1),
    (3, 0), (0, 2)
]

"""The DIBITS values each form four-bit values. Three of these four-bit values
are split into four three-bit values to be used as XOR masks for Polybius row
and column"""


def three(a, b, c):
    """Combine three dibit pairs into two tribit pairs."""
    a1, a2 = a
    assert 0 <= a1 <= 3, "a1 error: %s" % a1
    assert 0 <= a2 <= 3, "a1 error: %s" % a2

    b1, b2 = b
    assert 0 <= b1 <= 3, "b1 error: %s" % b1
    assert 0 <= b2 <= 3, "b1 error: %s" % b2

    c1, c2 = c
    assert 0 <= c1 <= 3, "c1 error: %s" % c1
    assert 0 <= c2 <= 3, "c1 error: %s" % c2

    n1 = a1 << 4 | a2 << 2 | b1
    n2 = b2 << 4 | c1 << 2 | c2
    n11, n12 = divmod(n1, 8)
    n21, n22 = divmod(n2, 8)
    return [(n11, n12), (n21, n22)]


def three2four(l):
    """Convert three dibit pairs to four tribit pairs."""
    #
    def generator(l):
        """Create a generator for the items in DIBITS."""
        for x in l:
            yield x

    g = generator(l)
    out = []

    for i in range(0, len(l), 3):
        b1 = next(g, (0, 0))
        b2 = next(g, (0, 0))
        b3 = next(g, (0, 0))
        # print(b1, b2, b3)
        out.extend(three(b1, b2, b3))

    return out

TRIBITS = three2four(DIBITS)

if __name__ == "__main__":

    from pprint import pprint
    import sys
    if sys.version_info > (3, 0):
        pprint(TRIBITS, width=76, compact=True)
    else:
        pprint(TRIBITS, width=76)

# end of file
