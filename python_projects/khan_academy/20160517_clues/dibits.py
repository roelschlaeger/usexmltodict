# coding=utf-8

"""This module contains the encoding of the cipher message."""

from __future__ import print_function

DEBUG = False

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

########################################################################


def binary6(item):
    """Convert numeric item into 6 character binary string."""
    out = []
    for _ in range(6):
        item, r = divmod(item, 2)
        out.append(chr(ord('0') + r))
    out.reverse()
    return "".join(out)

########################################################################


def print_binary_items(*items):
    """Convert all items to 6 character binary strings."""
    # print(items)
    line = []
    for item in items:
        line.append("".join(binary6(item)))
    print(line)

########################################################################


def hex(a, b, c):
    """Convert three 4-bit values to two 6-bit values."""
    a1, a2 = a
    assert 0 <= a1 <= 3, "a1 error: %s" % a1
    assert 0 <= a2 <= 3, "a2 error: %s" % a2

    b1, b2 = b
    assert 0 <= b1 <= 3, "b1 error: %s" % b1
    assert 0 <= b2 <= 3, "b2 error: %s" % b2

    c1, c2 = c
    assert 0 <= c1 <= 3, "c1 error: %s" % c1
    assert 0 <= c2 <= 3, "c2 error: %s" % c2

    o1 = a1 << 4 | a2 << 2 | b1
    o2 = b2 << 4 | c1 << 2 | c2

    if DEBUG:
        print_binary_items(a1, a2, b1, b2, c1, c2, o1, o2)

    return o1, o2

########################################################################


def three2two(l):
    """Convert three dibit pairs to two hexbit pairs."""
    #
    def generator():
        """Create a generator for the items in DIBITS."""
        for x in l:
            yield x

    g = generator()
    out = []

    for i in range(0, len(l), 3):
        a = next(g, (0, 0))
        b = next(g, (0, 0))
        c = next(g, (0, 0))
        # print(b1, b2, b3)
        out.extend(hex(a, b, c))

    return out

HEXBITS = three2two(DIBITS)

########################################################################

if __name__ == "__main__":

    from pprint import pprint
    import sys
    if sys.version_info > (3, 0):
        print("HEXBITS =")
        pprint(HEXBITS, width=76, compact=True)
    else:
        print("HEXBITS =")
        pprint(HEXBITS, width=76)

# end of file
