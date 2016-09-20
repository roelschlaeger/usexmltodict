# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

from __future__ import print_function

# https://py.checkio.org/mission/binary-count/

"""Count the number of 1's in a binary representation for a number."""


def checkio(n, a={}):
    """Count the number of 1's in a binary representation for a number."""

    count = 0
    while n:
        n = n & (n - 1)
        count += 1
    return count

assert checkio(4) == 1
assert checkio(15) == 4
assert checkio(1) == 1
assert checkio(1022) == 9
print("Done!")
