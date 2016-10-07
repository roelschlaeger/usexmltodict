# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/super-root/

# f(x) = x ** x - N
# f'(x) = (x ** x) * (ln(x) + 1)
#
# Newton's method
# x1 = x0 - f(x0) / f'(x0)
#
# Halley's # method
# x1 = x0 - 2 * f(x0) * f'(x0) / (2 * (f'(x0) ** 2)- f(x0) * f''(x0))

from __future__ import print_function

########################################################################

from math import log as ln

########################################################################

TABLE = dict([(x ** x, x) for x in range(11)])

########################################################################


def f(x, n):
    """The function."""
    return (x ** x) - n


########################################################################


def fp(x):
    """The derivative."""
    return (x ** x) * (ln(x) + 1)


########################################################################


def fpp(x):
    """The second derivative."""
    return (x ** x) * (ln(x) + 1) ** 2 + x ** (x - 1)


########################################################################


def super_root(n):
    """Approximate the root of n such that (root ** root) == n."""

    if n in TABLE:
        return TABLE[n]

    # make a starting guess
    for x in range(1, 11):
        if (x ** x) > n:
            break

    x0 = float(x - 1)
    x1 = float(x)

    while (abs(x1 - x0) > 0.001):
        x0 = x1
        x1 = (
            x0 -
            2 * f(x0, n) * fp(x0) /
            (2 * (fp(x0) ** 2) - f(x0, n) * fpp(x0))
        )

#   if round(x1, 3) == round(x1, 0):
#       x2 = int(x1)
#       if x2 ** x2 == n:
#           return x2

    return x1

########################################################################

if __name__ == "__main__":

    assert super_root(4) == 2
    assert super_root(27) == 3
    assert super_root(81) == 3.504339593597054
    assert super_root(10000000000L) == 10
    print("Done!")

# end of file
